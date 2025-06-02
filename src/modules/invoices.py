"""Módulo de generación de facturas"""
from PySide6.QtWidgets import QWidget, QMessageBox, QGridLayout, QVBoxLayout, QSizePolicy, QComboBox, QTableWidget, QTableWidgetItem, QHeaderView, QCheckBox, QHBoxLayout, QFileDialog
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from datetime import datetime, date
from clients import Client
from products import Product
from service import s
from styles.labels import LabelFactory
from styles.buttons import ButtonFactory
from styles.msg_boxes import MsgBoxFactory
from invoice_lib.templates import SimpleInvoice
from invoice_lib.models import ServiceProviderInfo, ClientInfo, InvoiceInfo, Item
import random, os
import polars as pl
from styles.lists import apply_table_style
from resource_util import resource_path

class Invoice(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.invoiceLayout = QVBoxLayout(self)
        self.invoiceLayout.setContentsMargins(10, 10, 10, 10)
        self.invoiceLayout.setSpacing(5)

        self.initUI()

    def initUI(self):
        self.initHeader()
        self.initFields()
        self.initButtons()
        self.initList()

    def initHeader(self):
        label = LabelFactory()

        self.headerLayout = QGridLayout()
        self.headerLayout.setContentsMargins(0, 0, 0, 0)
        self.headerLayout.setSpacing(0)

        self.invoice_label = label.create_label("Facturas", "Archivo Black", "bold_black", 32)
        self.headerLayout.addWidget(self.invoice_label, 0, 0, 1, 3, Qt.AlignLeft | Qt.AlignTop)

        self.invoice_sublabel = label.create_label("Genera tus facturas fácil y rápido", "Archivo Black", "bold_black", 16)
        self.headerLayout.addWidget(self.invoice_sublabel, 1, 0, 1, 3, Qt.AlignLeft | Qt.AlignTop)

        self.invoiceLayout.addLayout(self.headerLayout)

    def initButtons(self):
        button = ButtonFactory()
       
        self.btn_settings = button.create_button("", "default_black", resource_path("assets/icons/settings.png"), min_size = (75, 75))
        self.btn_settings.setToolTip("Ajustes")
        self.btn_settings.clicked.connect(self.open_settings)
        self.headerLayout.addWidget(self.btn_settings, 0, 3, Qt.AlignTop | Qt.AlignRight)
        
        self.btn_add_client = button.create_button("", "default_black", resource_path("assets/icons/add_client.png"), min_size=(75, 75))
        self.btn_add_client.clicked.connect(Client().add_client)
        self.fieldsLayout.addWidget(self.btn_add_client, 1, 1, Qt.AlignLeft)
        
        self.btn_add_product = button.create_button("", "default_black", resource_path("assets/icons/add_product.png"), min_size=(75, 75))
        self.btn_add_product.clicked.connect(Product().add_product)
        self.fieldsLayout.addWidget(self.btn_add_product, 1, 2, Qt.AlignLeft)
       
        self.btn_update_lists = button.create_button("", "default_black", resource_path("assets/icons/update.png"), min_size=(75, 75))
        self.btn_update_lists.clicked.connect(self.update_lists)
        self.fieldsLayout.addWidget(self.btn_update_lists, 1, 3, Qt.AlignLeft)
        
        self.btn_generate_invoice = button.create_button("Generar", "accept", None, 12, (100, 30))
        self.btn_generate_invoice.setStyleSheet(self.btn_generate_invoice.styleSheet() + """QPushButton {border: none; border-radius: 5px;}""")
        self.btn_generate_invoice.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.btn_generate_invoice.clicked.connect(self.generate_invoice)
        self.fieldsLayout.addWidget(self.btn_generate_invoice, 6, 1, 1, 4, Qt.AlignRight)
        
        descriptions = ["Agregar cliente", "Agregar producto", "Actualizar listas"]
        buttons = [self.btn_add_client, self.btn_add_product, self.btn_update_lists]
        
        for i, button in enumerate(buttons):
            button.setToolTip(descriptions[i])

    def initFields(self):
        label = LabelFactory()
        
        self.fieldsLayout = QGridLayout()
        self.fieldsLayout.setContentsMargins(0, 0, 0, 0)
        self.fieldsLayout.setSpacing(10)

        # Combobox de cliente
        self.client_combobox = QComboBox()
        self.client_combobox.setPlaceholderText("Seleccione un cliente")
        clients = s.get_client_by_id()

        for client in clients:
            self.client_combobox.addItem(f"{client[0]} - {client[1]}")
        
        self.client_combobox.setStyleSheet("""
            QComboBox {
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
                background-color: #f9f9f9;
            }
                QComboBox::drop-down {
                border-left: 1px solid #ccc;
                background-color: #e6e6e6;
                width: 14px;
            }
            QComboBox::down-arrow {
                width: 10px;
                height: 10px;
            }
            QComboBox QAbstractItemView {
                border: 1px solid #ccc;
                selection-background-color: #dcdcdc;
                background-color: #ffffff;
            }
        """)

        # Checkbox para marcar la factura como pagada
        self.paid_checkbox = QCheckBox("Marcar como pagado")
        self.paid_checkbox.setStyleSheet("""
                                        QCheckBox {
                                            font-size: 12px;
                                            padding: 5px;
                                            font-family: 'Archivo Medium';
                                        }""")
        
        self.fieldsLayout.addWidget(self.paid_checkbox, 5, 1, 1, 4, Qt.AlignRight)

        # Labels para mostrar datos del cliente seleccionado
        self.client_info_label = label.create_label("Información del Cliente", "Archivo Medium", "medium_black", 12)
        self.fieldsLayout.addWidget(self.client_info_label, 2, 0, Qt.AlignLeft)
        self.client_details_label = label.create_label("", "Archivo Medium", "medium_black", 12)
        self.fieldsLayout.addWidget(self.client_details_label, 3, 0, 2, Qt.AlignLeft)

        def update_client_details(index):
            if index >= 0:
                client_id = self.client_combobox.currentText().split(" - ")[0]
                query = f"SELECT id_cliente, nombre_cliente, email FROM cliente WHERE id_cliente = '{client_id}';"
                client_data = s.cur.execute(query).fetchone()
                self.client_details_label.setText(f"ID: {client_data[0]}     Nombre: {client_data[1]}"
                                                  f"\nEmail: {client_data[2]}")
        self.client_combobox.currentIndexChanged.connect(update_client_details)
        self.fieldsLayout.addWidget(self.client_combobox, 1, 0, Qt.AlignLeft)
        self.invoiceLayout.addLayout(self.fieldsLayout)
    
    def initList(self):
        l = LabelFactory()
        self.listLayout = QVBoxLayout()
        self.listLayout.setAlignment(Qt.AlignBottom)
        self.listLayout.setContentsMargins(0, 0, 0, 0)
        self.total_amount_label = l.create_label("Total: $0.00", "Archivo Medium", "money", 20)
        self.fieldsLayout.addWidget(self.total_amount_label, 4, 1, 1, 4, Qt.AlignRight)
        # Fetch data from the database usando Polars
        df = pl.read_database("SELECT id_producto, nombre, precio FROM producto;", s.conn)
        self.product_table = QTableWidget()
        self.product_table.setRowCount(df.height)
        self.product_table.setColumnCount(len(df.columns) + 2)
        self.product_table.setHorizontalHeaderLabels(["N°", "Nombre", "Precio", "Unidades", "Seleccionar"])
        self.product_table.setMinimumSize(600, 200)
        self.product_table.setContentsMargins(0, 0, 0, 0)
        self.product_table.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.product_table.setFont(QFont("Archivo Medium", 12))
        self.product_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.product_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.product_table.setSelectionMode(QTableWidget.SingleSelection)
        apply_table_style(self.product_table)

        for i in range(self.product_table.rowCount()):
            self.product_table.setRowHeight(i, 40)

        # Llenar la tabla con datos y agregar checkboxes usando Polars
        for i, row in enumerate(df.iter_rows()):
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                self.product_table.setItem(i, j, item)

            checkbox = QCheckBox()
            checkbox.stateChanged.connect(self.update_total_amount)
            checkbox_cell_widget = QWidget()
            checkbox_cell_layout = QHBoxLayout(checkbox_cell_widget)
            checkbox_cell_layout.setAlignment(Qt.AlignCenter)
            checkbox_cell_layout.setContentsMargins(0, 0, 0, 0)
            checkbox_cell_layout.addWidget(checkbox)

            self.product_table.setCellWidget(i, 4, checkbox_cell_widget)

            counter_cell_widget = QWidget()
            counter_cell_layout = QHBoxLayout(counter_cell_widget)
            counter_cell_layout.setAlignment(Qt.AlignCenter)
            counter_cell_layout.setContentsMargins(0, 0, 0, 0)

            btn_minus = ButtonFactory().create_button("-", "default_black", None, min_size=(10, 10))
            btn_plus = ButtonFactory().create_button("+", "default_black", None, min_size=(10, 10))
            unit_label = l.create_label("1", "Archivo Medium", "medium_black", 12)

            btn_minus.clicked.connect(lambda _, lbl=unit_label: (lbl.setText(str(max(0, int(lbl.text()) - 1))), self.update_total_amount()))
            btn_plus.clicked.connect(lambda _, lbl=unit_label: (lbl.setText(str(int(lbl.text()) + 1)), self.update_total_amount()))

            counter_cell_layout.addWidget(btn_minus)
            counter_cell_layout.addWidget(unit_label)
            counter_cell_layout.addWidget(btn_plus)

            self.product_table.setCellWidget(i, 3, counter_cell_widget)

        self.product_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.product_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)

        def handle_table_click(row, col):
            if col == 4:
                checkbox_cell_widget = self.product_table.cellWidget(row, col)
                if checkbox_cell_widget:
                    checkbox = checkbox_cell_widget.findChild(QCheckBox)
                    if checkbox:
                        checkbox.setChecked(not checkbox.isChecked())
        self.product_table.cellClicked.connect(handle_table_click)
        for i in range(self.product_table.rowCount()):
            price_item = self.product_table.item(i, 2)
            if price_item:
                price_item.setText(f"${{price_item.text()}}")
        self.update_total_amount()
        self.invoiceLayout.addLayout(self.listLayout)
        self.listLayout.addWidget(self.product_table)
        
    # Method to update the total amount
    def update_total_amount(self):
        total = 0
        for i in range(self.product_table.rowCount()):
            checkbox_cell_widget = self.product_table.cellWidget(i, 4)
            if checkbox_cell_widget:
                checkbox = checkbox_cell_widget.findChild(QCheckBox)
                if checkbox and checkbox.isChecked():
                    # Obtener el precio, eliminando el signo de dólar
                    price_item = self.product_table.item(i, 2)
                    price = float(price_item.text().replace('$', '')) if price_item else 0.0
                    # Obtener el valor del contador de unidades de la columna 3
                    counter_cell_widget = self.product_table.cellWidget(i, 3)
                    # Se asume que unit_label es un QLabel dentro del widget del contador.
                    unit_label = counter_cell_widget.findChild(type(self.total_amount_label))
                    if unit_label:
                        count = int(unit_label.text())
                    else:
                        count = 1  # en caso que no se encuentre, se suma al menos 1
                    total += price * count
                    
        self.total_amount_label.setText(f"Total: ${total:.2f}")
    
    def update_lists(self): #Método que actualiza la combobox y la lista
        l = LabelFactory()
        # Limpiar el label de detalles del cliente
        self.client_details_label.setText("")

        # Actualizar la combobox de clientes
        self.client_combobox.clear()
        clients = s.get_client_by_id()
        for client in clients:
            self.client_combobox.addItem(f"{client[0]} - {client[1]}")
        
        # Actualizar la tabla de productos usando Polars
        df = pl.read_database("SELECT id_producto, nombre, precio FROM producto;", s.conn)
        self.product_table.setRowCount(df.height)

        for i in range(self.product_table.rowCount()):
            self.product_table.setRowHeight(i, 40)

        for i, row in enumerate(df.iter_rows()):
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                self.product_table.setItem(i, j, item)
            #Actualizar las checkboxes
            checkbox = QCheckBox()
            checkbox.stateChanged.connect(self.update_total_amount)
            checkbox_cell_widget = QWidget()
            checkbox_cell_layout = QHBoxLayout(checkbox_cell_widget)
            checkbox_cell_layout.setAlignment(Qt.AlignCenter)
            checkbox_cell_layout.setContentsMargins(0, 0, 0, 0)
            checkbox_cell_layout.addWidget(checkbox)
            self.product_table.setCellWidget(i, 4, checkbox_cell_widget)
            
            #Actualizar el contador
            counter_cell_widget = QWidget()
            counter_cell_layout = QHBoxLayout(counter_cell_widget)
            counter_cell_layout.setAlignment(Qt.AlignCenter)
            counter_cell_layout.setContentsMargins(0, 0, 0, 0)
            btn_minus = ButtonFactory().create_button("-", "default_black", None, min_size=(10, 10))
            btn_plus = ButtonFactory().create_button("+", "default_black", None, min_size=(10, 10))
            unit_label = l.create_label("1", "Archivo Medium", "medium_black", 12)
            btn_minus.clicked.connect(lambda _, lbl=unit_label: (lbl.setText(str(max(0, int(lbl.text()) - 1))), self.update_total_amount()))
            btn_plus.clicked.connect(lambda _, lbl=unit_label: (lbl.setText(str(int(lbl.text()) + 1)), self.update_total_amount()))
            counter_cell_layout.addWidget(btn_minus)
            counter_cell_layout.addWidget(unit_label)
            counter_cell_layout.addWidget(btn_plus)
            self.product_table.setCellWidget(i, 3, counter_cell_widget)
            
        for i in range(self.product_table.rowCount()):
            price_item = self.product_table.item(i, 2)
            if price_item:
                # Evitamos agregar doble dólar si ya lo contiene
                if not price_item.text().startswith("$"):
                    price_item.setText(f"${price_item.text()}")

    def generate_invoice(self):
        msg = MsgBoxFactory()
        now = datetime.now()
        q = msg.create_question_box("question", "Generar factura", "¿Desea generar la factura?", QMessageBox.Question,
                                    "Archivo Medium", 12, ["Confirmar", "Cancelar"], [QMessageBox.AcceptRole, QMessageBox.RejectRole])
        q.exec()
        if q.clickedButton().text() == "Confirmar":
            try:
                # Validaciones previas antes de generar la factura
                selected_client = bool(self.client_combobox.currentText())
                selected_products = any(
                    self.product_table.cellWidget(i, 4).findChild(QCheckBox).isChecked()
                    for i in range(self.product_table.rowCount())
                )
                service_provider_data = s.cur.execute("SELECT nombre, nit, direccion, telefono, email FROM proveedor;").fetchone()
                
                if not selected_client and not selected_products:
                    r = msg.create_msg_box(
                        "warning", "Advertencia", "Debe seleccionar un cliente y al menos un producto.",
                        QMessageBox.Warning, "Archivo Medium", 12, "Aceptar", QMessageBox.AcceptRole
                    )
                    r.exec()
                    return
                elif not selected_client:
                    r = msg.create_msg_box(
                        "warning", "Advertencia", "Debe seleccionar un cliente antes de generar la factura.",
                        QMessageBox.Warning, "Archivo Medium", 12, "Aceptar", QMessageBox.AcceptRole
                    )
                    r.exec()
                    return
                elif not selected_products:
                    r = msg.create_msg_box(
                        "warning", "Advertencia", "Debe seleccionar al menos un producto en la lista.",
                        QMessageBox.Warning, "Archivo Medium", 12, "Aceptar", QMessageBox.AcceptRole
                    )
                    r.exec()
                    return

                # Obtener datos del cliente y los productos seleccionados
                client_id = self.client_combobox.currentText().split(" - ")[0]
                product_ids = [self.product_table.item(i, 0).text() for i in range(self.product_table.rowCount()) if self.product_table.cellWidget(i, 4).findChild(QCheckBox).isChecked()]
                
                query = f"SELECT id_cliente, nombre_cliente, email, direccion, telefono, cedula FROM cliente WHERE id_cliente = '{client_id}';"
                query2 = f"SELECT id_producto, nombre, precio, descripcion FROM producto WHERE id_producto IN ({', '.join(['?' for _ in product_ids])});"
                query3 = f"SELECT nombre, nit, direccion, telefono, email from proveedor;"

                client_data = s.cur.execute(query).fetchone()
                product_data = s.cur.execute(query2, product_ids).fetchall()
                service_provider_data = s.cur.execute(query3).fetchone()

                invoice_id = f"INV-{random.randint(100, 999)}"
                invoice_datetime = now.strftime("%d/%m/%Y")
                due_datetime = now.strftime("%d/%m/%Y")

                #Agregar la información del cliente y el proveedor de servicios
                doc = SimpleInvoice(f"{invoice_id}.pdf")
                doc.invoice_info = InvoiceInfo(invoice_id=invoice_id, invoice_datetime=invoice_datetime, due_datetime=due_datetime)

                for product in product_data:
                    # Obtener las unidades seleccionadas desde unit_label
                    row_index = next((i for i in range(self.product_table.rowCount()) if self.product_table.item(i, 0).text() == product[0]), None)
                    if row_index is not None:
                        counter_cell_widget = self.product_table.cellWidget(row_index, 3)
                        unit_label = counter_cell_widget.findChild(type(self.total_amount_label))
                        units = int(unit_label.text()) if unit_label else 1
                        doc.add_item(Item(product[1], product[3], units, float(product[2])))

                doc.client_info = ClientInfo(client_id=client_data[0], name=client_data[1], vat_tax_number=client_data[5], street=client_data[3], phone=client_data[4] , email=client_data[2])
                doc.service_provider_info = ServiceProviderInfo(name=service_provider_data[0], vat_tax_number=service_provider_data[1], street=service_provider_data[2], phone=service_provider_data[3], email=service_provider_data[4])
                tax = 5
                doc.set_item_tax_rate(tax)
                doc.set_bottom_tip("Gracias por su compra!")

                # Evaluar si la factura está pagada
                doc.is_paid = self.paid_checkbox.isChecked()
                
                # Abrir un diálogo para seleccionar la carpeta de guardado
                default_filename = f"{invoice_id}.pdf"
                save_path, _ = QFileDialog.getSaveFileName(
                    self,
                    "Seleccionar carpeta para guardar la factura",
                    os.path.join(os.path.expanduser("~"), default_filename),
                    "PDF files (*.pdf)"
                )
                save_dir = os.path.dirname(save_path) if save_path else ""
                
                if save_path and not save_path.lower().endswith(".pdf"):
                    save_path += ".pdf"

                if not save_dir:
                    return  # El usuario canceló, no generar la factura

                pdf_path = os.path.join(save_dir, f"{invoice_id}.pdf")
                
                doc.filename = pdf_path  # Asegura que el PDF se guarde en la ruta seleccionada
                doc.finish()

                subtotal = sum(float(product[2]) * unidades for product, unidades in zip(product_data, [int(self.product_table.cellWidget(i, 3).findChild(type(self.total_amount_label)).text()) for i in range(self.product_table.rowCount()) if self.product_table.cellWidget(i, 4).findChild(QCheckBox).isChecked()]))

                total = subtotal * (1 + tax / 100)

                self.save_invoice(
                    invoice_id=invoice_id,
                    fecha_emision=invoice_datetime,
                    id_cliente=client_data[0],
                    id_producto=",".join(product_ids),
                    pdf_path=pdf_path,
                    emisor=service_provider_data[0],
                    subtotal=subtotal,
                    iva=tax,
                    total=total
                )
                r = msg.create_msg_box("information", "Información", "Factura creada correctamente",
                                    QMessageBox.Information, "Archivo Medium", 12, "Aceptar", QMessageBox.AcceptRole)
                r.exec()
            
            except Exception as e:
                if not service_provider_data:
                    r = msg.create_question_box(
                        "warning", "Advertencia", "No se ha configurado un proveedor de servicios. ¿Desea configurarlo ahora?",
                        QMessageBox.Warning, "Archivo Medium", 12, ["Sí", "No"], [QMessageBox.AcceptRole, QMessageBox.RejectRole]
                    )
                    r.exec()
                    
                    if r.clickedButton().text() == "Sí":
                        from settings import SettingsWindow
                        self.settings_window = SettingsWindow()
                        self.settings_window.set_provider_info()
                        self.settings_window.provider_saved.connect(
                            lambda saved: (
                                self.generate_invoice() if saved else
                                msg.create_msg_box(
                                    "warning", "Cancelado", "La operación fue cancelada y la factura no se generó.",
                                    QMessageBox.Warning, "Archivo Medium", 12, "Aceptar", QMessageBox.AcceptRole
                                ).exec()
                            )
                        )
                    else:
                        return
                else:
                    error_msg = f"Error al generar la factura: {str(e)}"
                    r = msg.create_msg_box("error", "Error", error_msg, QMessageBox.Critical, "Archivo Medium", 12, "Aceptar", QMessageBox.AcceptRole)
                    r.exec()

        else:
            pass    

    def save_invoice(self, invoice_id, fecha_emision, id_cliente, id_producto, pdf_path, emisor, subtotal, iva, total):
        # Lee el PDF como binario
        with open(pdf_path, "rb") as f:
            pdf_blob = f.read()

        # Guarda en la base de datos usando el método del servicio
        s.insert_invoice(
            id_factura=invoice_id, fecha_emision=fecha_emision, id_cliente=id_cliente, id_producto=id_producto,
            comprobante=pdf_blob, emisor=emisor, subtotal=subtotal, iva=iva,total=total
        )

        # Actualiza la lista de facturas del módulo invoice_mgmt.py
        from invoices_mgmt import InvoiceMgmt
        if hasattr(self, 'invoice_mgmt'):
            self.invoice_mgmt.update_list_on_change()
        else:
            self.invoice_mgmt = InvoiceMgmt()
            self.invoice_mgmt.update_list_on_change()

    def open_settings(self):
        from settings import SettingsWindow
        self.settings_window = SettingsWindow()
        self.settings_window.show()