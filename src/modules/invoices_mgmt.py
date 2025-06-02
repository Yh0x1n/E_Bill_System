"""MÓDULO DE GESTIÓN DE FACTURAS"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QTableWidget, QSizePolicy, QTableWidgetItem, QHeaderView, QMessageBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from styles.labels import LabelFactory
from styles.buttons import ButtonFactory
from styles.msg_boxes import MsgBoxFactory
from styles.lists import apply_table_style
from export import Export
from service import s
from resource_util import resource_path
import polars as pl
import os, sys, tempfile

class InvoiceMgmt(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.invoiceLayout = QVBoxLayout(self)
        self.invoiceLayout.setContentsMargins(10, 10, 10, 10)
        self.invoiceLayout.setSpacing(5)
        self.initUI()

    def initUI(self):
        self.initHeader()
        self.initButtons()
        self.initList()

    def initHeader(self):
        label = LabelFactory()
        self.headerLayout = QGridLayout()
        self.invoice_label = label.create_label("Facturas", "Archivo Black", "bold_black", 32)
        self.headerLayout.addWidget(self.invoice_label, 0, 0, 1, 3, Qt.AlignLeft)
        self.invoice_sublabel = label.create_label("Administra tus facturas", "Archivo Black", "bold_black", 16)
        self.headerLayout.addWidget(self.invoice_sublabel, 1, 0, 1, 3, Qt.AlignLeft)
        self.invoiceLayout.addLayout(self.headerLayout)

    def initButtons(self):
        button = ButtonFactory()
        self.buttonLayout = QGridLayout()
        self.buttonLayout.setContentsMargins(0, 100, 0, 0)
        self.buttonLayout.setSpacing(5)
        self.buttonLayout.setAlignment(Qt.AlignBottom)
        self.invoiceLayout.addLayout(self.buttonLayout)
        self.btn_settings = button.create_button("", "default_black", resource_path("assets/icons/settings.png"), min_size=(75, 75))
        self.btn_settings.setToolTip("Ajustes")
        self.btn_settings.clicked.connect(self.open_settings)
        self.headerLayout.addWidget(self.btn_settings, 0, 3, 2, 2, Qt.AlignTop | Qt.AlignRight)
        self.btn_delete = button.create_button("", "default_black", resource_path("assets/icons/Trash.png"), min_size=(75, 75))
        self.btn_delete.clicked.connect(self.delete_invoice)
        self.buttonLayout.addWidget(self.btn_delete, 4, 5, 3, 4, Qt.AlignBottom | Qt.AlignRight)
        self.btn_export = button.create_button("", "default_black", resource_path("assets/icons/excel.png"), min_size=(75, 75))
        self.btn_export.clicked.connect(self.export)
        self.buttonLayout.addWidget(self.btn_export, 4, 6, 3, 4, Qt.AlignBottom | Qt.AlignRight)
        description = ["Eliminar", "Ajustes", "Exportar a Excel"]
        buttons = [self.btn_delete, self.btn_settings, self.btn_export]
        for i, button in enumerate(buttons):
            button.setToolTip(description[i])

    def initList(self):
        button = ButtonFactory()
        self.listLayout = QVBoxLayout()
        self.listLayout.setAlignment(Qt.AlignBottom)
        self.listLayout.setContentsMargins(0, 0, 0, 0)
        self.invoiceLayout.addLayout(self.listLayout)
        
        # Fetch data from the database usando Polars
        df = pl.read_database(
            """
            SELECT f.id_factura, f.fecha_emision, c.nombre_cliente AS cliente, f.total
            FROM facturas f
            JOIN cliente c ON f.id_cliente = c.id_cliente;
            """,
            s.conn
        )
        
        self.invoice_table = QTableWidget()
        self.invoice_table.setRowCount(df.height)
        self.invoice_table.setColumnCount(len(df.columns) + 1)
        self.invoice_table.setHorizontalHeaderLabels(["N°", "Fecha", "Cliente", "Total", ""])
        self.invoice_table.setMinimumSize(600, 200)
        self.invoice_table.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.invoice_table.setFont(QFont("Archivo Medium", 12))
        self.invoice_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.invoice_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.invoice_table.setSelectionMode(QTableWidget.SingleSelection)
        
        for i, row in enumerate(df.iter_rows()):
            for j, value in enumerate(row):
                self.invoice_table.setItem(i, j, QTableWidgetItem(str(value)))
        
        self.invoice_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        for i in range(self.invoice_table.rowCount()):
            total_item = self.invoice_table.item(i, 3)
            if total_item:
                try:
                    # Eliminar el símbolo $ y comas si existen
                    text = total_item.text().replace('$', '').replace(',', '').strip()
                    total_value = float(text)
                    total_item.setText(f"${total_value:.2f}")
                except Exception:
                    pass

            open_btn = button.create_button("Abrir", "default_black", None, font_size=10, min_size=(75, 20))
            open_btn.setStyleSheet("QPushButton {border-radius: 5px; color: white; background-color: #0071BD; text-align: center; } QPushButton:hover { background-color: darkblue; }")
            open_btn.clicked.connect(lambda _, row=i: self.mostrar_factura_db(self.invoice_table.item(row, 0).text()))

            self.invoice_table.setCellWidget(i, 4, open_btn)

        self.listLayout.addWidget(self.invoice_table)
        self.invoice_table.itemDoubleClicked.connect(lambda _: self.show_details())
        
        self.invoice_table.keyPressEvent = self._invoice_table_key_press_event
        
        apply_table_style(self.invoice_table)
        
        self.update_list_on_change()

    def _invoice_table_key_press_event(self, event):
        if event.key() == Qt.Key_Delete:
            self.delete_invoice()
        else:
            super(QTableWidget, self.invoice_table).keyPressEvent(event)

    def delete_invoice(self):
        msgbox = MsgBoxFactory()
        selected_items = self.invoice_table.selectedItems()
        
        if not selected_items:
            q = msgbox.create_msg_box("information", "Información", "Selecciona una factura a eliminar.", QMessageBox.Information, "Archivo Medium", 12, "Aceptar", QMessageBox.AcceptRole)
            q.exec()
            return
        
        row = selected_items[0].row()
        invoice_id_item = self.invoice_table.item(row, 0)
        invoice_id = invoice_id_item.text()
        
        try:
            q = msgbox.create_question_box("question", "Información", "¿Desea eliminar esta factura?", QMessageBox.Question, "Archivo Medium", 12, ["Sí", "No"], [QMessageBox.AcceptRole, QMessageBox.RejectRole])
            q.exec()
        
            if q.clickedButton().text() == "Sí":
                # Eliminar la factura de la base de datos
                s.cur.execute("DELETE FROM facturas WHERE id_factura = ?", (invoice_id,))
                s.conn.commit()

                # Eliminar la fila de la tabla en la interfaz
                self.invoice_table.removeRow(row)

                # Mostrar mensaje de éxito
                msgbox.create_msg_box("information", "Éxito", "La factura ha sido eliminada correctamente.", QMessageBox.Information,
                                        "Archivo Medium", 12, "Aceptar", QMessageBox.AcceptRole).exec()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo eliminar la factura: {e}")

    def show_details(self):
        # Obtener el ID de la factura seleccionada
        selected_items = self.invoice_table.selectedItems()
        
        if not selected_items:
            return
        
        row = selected_items[0].row()
        invoice_id = self.invoice_table.item(row, 0).text()
        
        # Obtener los detalles desde la base de datos
        details = s.cur.execute("""
            SELECT f.id_factura, f.fecha_emision, c.nombre_cliente, f.total
            FROM facturas f
            JOIN cliente c ON f.id_cliente = c.id_cliente
            WHERE f.id_factura = ?
        """, (invoice_id,)).fetchone()
        
        if not details:
            return
        
        labels = ["ID", "Fecha", "Cliente", "Total"]
        details_text = ""
        
        for i, detail in enumerate(details):
            if labels[i] == "Total":
                details_text += f"<b>{labels[i]}:</b> ${float(detail):.2f}<br>"
            
            else:
                details_text += f"<b>{labels[i]}:</b> {detail}<br>"
       
        provider_name = s.cur.execute("SELECT nombre FROM proveedor;").fetchone()
       
        if provider_name:
            details_text += f"<b>Emisor:</b> {provider_name[0]}<br>"
        
        msgbox = MsgBoxFactory()
        msg = msgbox.create_msg_box(
            "information",
            "Detalles de la Factura",
            f"<h3>Detalles de la Factura</h3><p>{details_text}</p>",
            QMessageBox.NoIcon, "Archivo Medium", 12, "Volver", QMessageBox.AcceptRole
        )
        msg.exec()

    def mostrar_factura_db(self, factura_id):
        # Extrae el PDF de la base de datos y lo abre con el visor predeterminado
        result = s.cur.execute("""
            SELECT comprobante FROM facturas WHERE id_factura = ?
        """, (factura_id,)).fetchone()

        if not result or not result[0]:
            MsgBoxFactory().create_msg_box("error", "Error", "No se encontró el PDF de la factura.",
                                           QMessageBox.Critical, "Archivo Medium", 12, "Aceptar",
                                           QMessageBox.AcceptRole).exec()
            return

        pdf_data = result[0]

        with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{factura_id}.pdf") as tmp:
            tmp.write(pdf_data)
            tmp_path = tmp.name

        # Abrir el PDF con el visor predeterminado del sistema
        if sys.platform.startswith('win'):
            os.startfile(tmp_path)

        elif sys.platform.startswith('darwin'):
            os.system(f'open "{tmp_path}"')

        else:
            os.system(f'xdg-open "{tmp_path}"')

    def export(self):
        Export().export_data("invoices")
    
    def open_settings(self):
        from settings import SettingsWindow
        self.settings_window = SettingsWindow()
        self.settings_window.show()

    def update_list_on_change(self):
        """Actualiza la lista de facturas cuando se realizan cambios y al entrar al módulo (cuando se guardan nuevas facturas)."""
        df = pl.read_database("""SELECT f.id_factura, f.fecha_emision, c.nombre_cliente AS cliente, f.total
                        FROM facturas f JOIN cliente c ON f.id_cliente = c.id_cliente;""", s.conn)
        self.invoice_table.setRowCount(df.height)
        for i, row in enumerate(df.iter_rows()):
            for j, value in enumerate(row):
                self.invoice_table.setItem(i, j, QTableWidgetItem(str(value)))