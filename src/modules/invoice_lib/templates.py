from __future__ import unicode_literals
from datetime import datetime, date
from decimal import Decimal

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, Spacer

from invoice_lib.components import SimpleTable, TableWithHeader, PaidStamp
from invoice_lib.models import PDFInfo, Item, Transaction, InvoiceInfo, ServiceProviderInfo, ClientInfo
from resource_util import resource_path

import os

class SimpleInvoice(SimpleDocTemplate):
    default_pdf_info = PDFInfo(title='Factura', author='RossTech Solutions', subject='Factura')
    precision = None

    def __init__(self, invoice_path, pdf_info=None, precision='0.01'):
        if not pdf_info:
            pdf_info = self.default_pdf_info

        SimpleDocTemplate.__init__(
            self,
            invoice_path,
            pagesize=letter,
            rightMargin=inch,
            leftMargin=inch,
            topMargin=inch,
            bottomMargin=inch,
            **pdf_info.__dict__
        )

        self.precision = precision

        self._defined_styles = getSampleStyleSheet()
        self._defined_styles.add(
            ParagraphStyle('RightHeading1', parent=self._defined_styles.get('Heading1'), alignment=TA_RIGHT)
        )
        self._defined_styles.add(
            ParagraphStyle('TableParagraph', parent=self._defined_styles.get('Normal'), alignment=TA_CENTER)
        )

        self.invoice_info = None
        self.service_provider_info = None
        self.client_info = None
        self.is_paid = False
        self._items = []
        self._item_tax_rate = None
        self._transactions = []
        self._story = []
        self._bottom_tip = None
        self._bottom_tip_align = None

    @property
    def items(self):
        return self._items[:]

    def add_item(self, item):
        if isinstance(item, Item):
            self._items.append(item)

    def set_item_tax_rate(self, rate):
        self._item_tax_rate = rate

    @property
    def transactions(self):
        return self._transactions[:]

    def add_transaction(self, t):
        if isinstance(t, Transaction):
            self._transactions.append(t)

    def set_bottom_tip(self, text, align=TA_CENTER):
        self._bottom_tip = text
        self._bottom_tip_align = align

    @staticmethod
    def _format_value(value):
        if isinstance(value, datetime):
            value = value.strftime('%Y-%m-%d %H:%M')
        elif isinstance(value, date):
            value = value.strftime('%Y-%m-%d')
        return value

    def _attribute_to_table_data(self, instance, attribute_verbose_name_list):
        data = []

        for property_name, verbose_name in attribute_verbose_name_list:
            attr = getattr(instance, property_name, None)
            if attr:
                attr = self._format_value(attr)
                data.append(['{0}:'.format(verbose_name), attr])

        return data

    def _invoice_info_data(self):
        if isinstance(self.invoice_info, InvoiceInfo):
            props = [('invoice_id', 'N° de Factura'), ('invoice_datetime', 'Fecha de emisión'),
                     ('due_datetime', 'Fecha de vencimiento')]

            return self._attribute_to_table_data(self.invoice_info, props)

        return []

    def _build_invoice_info(self):
        invoice_info_data = self._invoice_info_data()
        if invoice_info_data:
            self._story.append(Paragraph('Factura de Venta', self._defined_styles.get('RightHeading1')))
            self._story.append(SimpleTable(invoice_info_data, horizontal_align='RIGHT'))

    def _service_provider_data(self):
        if isinstance(self.service_provider_info, ServiceProviderInfo):
            props = [
                ('name', 'Nombre'),
                ('street', 'Dirección'),
                ('city', 'Ciudad'),
                ('state', 'Estado/Dpto.'),
                ('country', 'País'),
                ('post_code', 'Código postal'),
                ('vat_tax_number', 'NIT'),
                ('email', 'Correo electrónico'),
                ('phone_number', "Teléfono"),
                ('fiscal_regime', 'Régimen Fiscal'),
                ('tax_responsibility', 'Responsabilidad Tributaria'),
                ('economic_activity', 'Actividad Económica')
            ]

            return self._attribute_to_table_data(self.service_provider_info, props)

        return []

    def _build_service_provider_info(self):
        # Merchant
        service_provider_info_data = self._service_provider_data()
        if service_provider_info_data:
            self._story.append(Paragraph('Datos del Emisor', self._defined_styles.get('RightHeading1')))
            self._story.append(SimpleTable(service_provider_info_data, horizontal_align='RIGHT'))

    def _client_info_data(self):
        if not isinstance(self.client_info, ClientInfo):
            return []

        props = [
            ('name', 'Nombre'),
            ('street', 'Dirección'),
            ('city', 'Ciudad'),
            ('state', 'Estado/Dpto.'),
            ('country', 'País'),
            ('post_code', 'Código postal'),
            ('email', 'Correo electrónico'),
            ('client_id', 'N° Cliente'),
            ('vat_tax_number', 'NIT'),
            ('phone_number', "Teléfono")
        ]
        # Añadir solo los campos opcionales si tienen valor
        if getattr(self.client_info, 'fiscal_regime', None):
            props.append(('fiscal_regime', 'Régimen Fiscal'))
        if getattr(self.client_info, 'tax_responsibility', None):
            props.append(('tax_responsibility', 'Responsabilidad Tributaria'))
        if getattr(self.client_info, 'economic_activity', None):
            props.append(('economic_activity', 'Actividad Económica'))
        return self._attribute_to_table_data(self.client_info, props)

    def _build_client_info(self):
        # ClientInfo
        client_info_data = self._client_info_data()
        if client_info_data:
            self._story.append(Paragraph('Datos del Cliente', self._defined_styles.get('Heading1')))
            self._story.append(SimpleTable(client_info_data, horizontal_align='LEFT'))

    def _build_service_provider_and_client_info(self):
        if isinstance(self.service_provider_info, ServiceProviderInfo) and isinstance(self.client_info, ClientInfo):
            # Merge Table
            table_data = [
                [
                    Paragraph('Datos del Emisor', self._defined_styles.get('Heading1')), '',
                    '',
                    Paragraph('Datos del Cliente', self._defined_styles.get('Heading1')), ''
                ]
            ]
            table_style = [
                ('SPAN', (0, 0), (1, 0)),
                ('SPAN', (3, 0), (4, 0)),
                ('LINEBELOW', (0, 0), (1, 0), 1, colors.gray),
                ('LINEBELOW', (3, 0), (4, 0), 1, colors.gray),
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ]
            client_info_data = self._client_info_data()
            service_provider_data = self._service_provider_data()
            diff = abs(len(client_info_data) - len(service_provider_data))
            if diff > 0:
                if len(client_info_data) < len(service_provider_data):
                    client_info_data.extend([["", ""]]*diff)
                else:
                    service_provider_data.extend([["", ""]*diff])
            for d in zip(service_provider_data, client_info_data):
                d[0].append('')
                d[0].extend(d[1])
                table_data.append(d[0])
            self._story.append(
                Table(table_data, style=table_style)
            )
        else:
            self._build_service_provider_info()
            self._build_client_info()

    def _item_raw_data_and_subtotal(self):
        item_data = []
        item_subtotal = 0

        for item in self._items:
            if not isinstance(item, Item):
                continue

            item_data.append(
                (
                    item.name,
                    Paragraph(item.description, self._defined_styles.get('TableParagraph')),
                    item.units,
                    item.unit_price,
                    item.amount
                )
            )
            item_subtotal += item.amount

        return item_data, item_subtotal

    def _item_data_and_style(self):
        # Items
        item_data, item_subtotal = self._item_raw_data_and_subtotal()
        style = []

        if not item_data:
            return item_data, style

        self._story.append(
            Paragraph('Detalles de Producto/Servicio', self._defined_styles.get('Heading1'))
        )

        item_data_title = ('Nombre', 'Descripción', 'Unidades', 'Precio por unidad', 'Monto')
        item_data.insert(0, item_data_title)  # Insert title

        # Summary field
        sum_start_y_index = len(item_data)
        sum_end_x_index = -1 - 1
        sum_start_x_index = len(item_data_title) - abs(sum_end_x_index)

        # ##### Subtotal #####
        rounditem_subtotal = self.getroundeddecimal(item_subtotal, self.precision)
        item_data.append(
            ('Subtotal', '$', '', '', rounditem_subtotal)
        )

        style.append(('SPAN', (0, sum_start_y_index), (sum_start_x_index, sum_start_y_index)))
        style.append(('ALIGN', (0, sum_start_y_index), (sum_end_x_index, -1), 'RIGHT'))

        # Tax total
        if self._item_tax_rate is not None:
            tax_total = item_subtotal * (Decimal(str(self._item_tax_rate)) / Decimal('100'))
            roundtax_total = self.getroundeddecimal(tax_total, self.precision)
            item_data.append(
                ('IVA ({0}%)'.format(self._item_tax_rate), '', '', '', roundtax_total)
            )
            sum_start_y_index += 1
            style.append(('SPAN', (0, sum_start_y_index), (sum_start_x_index, sum_start_y_index)))
            style.append(('ALIGN', (0, sum_start_y_index), (sum_end_x_index, -1), 'RIGHT'))
        else:
            tax_total = None

        # Total
        total = item_subtotal + (tax_total if tax_total else Decimal('0'))
        roundtotal = self.getroundeddecimal(total, self.precision)
        item_data.append(('Total', '$', '', '', roundtotal))
        sum_start_y_index += 1
        style.append(('SPAN', (0, sum_start_y_index), (sum_start_x_index, sum_start_y_index)))
        style.append(('ALIGN', (0, sum_start_y_index), (sum_end_x_index, -1), 'RIGHT'))

        return item_data, style

    def getroundeddecimal(self, nrtoround, precision):
        d = Decimal(nrtoround)
        aftercomma = Decimal(precision) # or anything that has the exponent depth you want
        rvalue = Decimal(d.quantize(aftercomma, rounding='ROUND_HALF_UP'))
        return rvalue

    def _build_items(self):
        item_data, style = self._item_data_and_style()
        if item_data:
            self._story.append(TableWithHeader(item_data, horizontal_align='LEFT', style=style))

    def _transactions_data(self):
        transaction_table_data = [
            (
                t.transaction_id,
                Paragraph(t.gateway, self._defined_styles.get('TableParagraph')),
                self._format_value(t.transaction_datetime),
                t.amount,
            ) for t in self._transactions if isinstance(t, Transaction)
        ]

        if transaction_table_data:
            transaction_table_data.insert(0, ('Transaction id', 'Gateway', 'Transaction date', 'Amount'))

        return transaction_table_data

    def _build_transactions(self):
        # Transaction
        transaction_table_data = self._transactions_data()

        if transaction_table_data:
            self._story.append(Paragraph('Transaction', self._defined_styles.get('Heading1')))
            self._story.append(TableWithHeader(transaction_table_data, horizontal_align='LEFT'))

    def _build_bottom_tip(self):
        if self._bottom_tip:
            self._story.append(Spacer(5, 5))
            self._story.append(
                Paragraph(
                    self._bottom_tip,
                    ParagraphStyle(
                        'BottomTip',
                        parent=self._defined_styles.get('Normal'),
                        alignment=self._bottom_tip_align
                    )
                )
            )
    
    def _build_bottom_tip(self):
        if self._bottom_tip:
            self._story.append(Spacer(5, 5))
            self._story.append(
                Paragraph(
                    self._bottom_tip,
                    ParagraphStyle(
                        'BottomTip',
                        parent=self._defined_styles.get('Normal'),
                        alignment=self._bottom_tip_align
                    )
                )
            )

    def add_image(self, image_path, width, height):
        """
        Agrega una imagen al documento.
        
        :param image_path: Ruta de la imagen.
        :param width: Ancho de la imagen en puntos.
        :param height: Alto de la imagen en puntos.
        """
        from reportlab.platypus import Image
        img = Image(image_path)
        img.drawWidth = width
        img.drawHeight = height
        self._story.append(img)

    def finish(self):
        self._story = []
        self._build_invoice_info()
        self._build_service_provider_and_client_info()
        self._build_items()
        self._build_transactions()
        self._build_bottom_tip()
        # Usar resource_path para la imagen del logo
        logo_path = resource_path("assets/pictures/AqualabLogo.jpg")
        self.add_image(logo_path, 50, 50)
        kwargs = {}
        if self.is_paid:
            kwargs['onFirstPage'] = PaidStamp(7 * inch, 5.8 * inch)
        self.build(self._story, **kwargs)