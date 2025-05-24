"""MÓDULO DE GESTIÓN DE FACTURAS"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QTableWidget, QSizePolicy, QTableWidgetItem, QHeaderView, QMessageBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from styles.labels import LabelFactory
from styles.buttons import ButtonFactory
from styles.msg_boxes import MsgBoxFactory
from styles.lists import apply_table_style
from export import Export

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

        self.btn_settings = button.create_button("", "default_black", "src/assets/icons/settings.png", min_size=(75, 75))
        self.btn_settings.setToolTip("Ajustes")
        self.btn_settings.clicked.connect(self.open_settings)
        self.headerLayout.addWidget(self.btn_settings, 0, 3, 2, 2, Qt.AlignTop | Qt.AlignRight)

        self.btn_delete = button.create_button("", "default_black", "src/assets/icons/Trash.png", min_size=(75, 75))
        self.btn_delete.clicked.connect(self.delete_invoice)
        self.buttonLayout.addWidget(self.btn_delete, 4, 5, 3, 4, Qt.AlignBottom | Qt.AlignRight)

        self.btn_export = button.create_button("", "default_black", "src/assets/icons/excel.png", min_size=(75, 75))
        self.btn_export.clicked.connect(self.export)
        self.buttonLayout.addWidget(self.btn_export, 4, 6, 3, 4, Qt.AlignBottom | Qt.AlignRight)

        description = ["Eliminar", "Ajustes", "Exportar a Excel"]
        buttons = [self.btn_delete, self.btn_settings, self.btn_export]
        for i, button in enumerate(buttons):
            button.setToolTip(description[i])

    def initList(self):
        from service import s
        self.listLayout = QVBoxLayout()
        self.listLayout.setAlignment(Qt.AlignBottom)
        self.listLayout.setContentsMargins(0, 0, 0, 0)
        self.invoiceLayout.addLayout(self.listLayout)
        # Fetch data from the database
        import pandas as pd
        df = pd.read_sql(
            """
            SELECT f.id_factura, f.fecha_emision, c.nombre_cliente AS cliente, f.total
            FROM facturas f
            JOIN cliente c ON f.id_cliente = c.id_cliente;
            """,
            s.conn
        )
        self.invoice_table = QTableWidget()
        self.invoice_table.setRowCount(len(df))
        self.invoice_table.setColumnCount(len(df.columns))
        self.invoice_table.setHorizontalHeaderLabels(["N°", "Fecha", "Cliente", "Total"])
        self.invoice_table.setMinimumSize(600, 200)
        self.invoice_table.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.invoice_table.setFont(QFont("Archivo Medium", 12))
        self.invoice_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.invoice_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.invoice_table.setSelectionMode(QTableWidget.SingleSelection)
        for i, row in df.iterrows():
            for j, value in enumerate(row):
                self.invoice_table.setItem(i, j, QTableWidgetItem(str(value)))
        self.invoice_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        for i in range(self.invoice_table.rowCount()):
            total_item = self.invoice_table.item(i, 3)
            if total_item:
                try:
                    total_value = float(total_item.text())
                    total_item.setText(f"${total_value:.2f}")
                except ValueError:
                    total_item.setText(f"${total_item.text()}")
        self.listLayout.addWidget(self.invoice_table)
        self.invoice_table.itemDoubleClicked.connect(lambda _: self.show_details())
        apply_table_style(self.invoice_table)

    def delete_invoice(self):
        from service import s
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
                # Implementa aquí la lógica para eliminar la factura de la base de datos
                pass
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo eliminar la factura: {e}")

    def show_details(self):
        from service import s
        import pandas as pd

        selected_items = self.invoice_table.selectedItems()
        if not selected_items:
            return
        
        row = selected_items[0].row()
        invoice_id = self.invoice_table.item(row, 0).text()
        
        # Obtener los detalles completos de la factura desde la base de datos usando el ID seleccionado
        query = """
            SELECT f.id_factura, f.fecha_emision, c.nombre_cliente AS cliente, f.total
            FROM facturas f
            JOIN cliente c ON f.id_cliente = c.id_cliente
            WHERE f.id_factura = ?;
        """
        df = pd.read_sql(query, s.conn, params=[invoice_id])
        if not df.empty:
            invoice_date = df.at[0, "fecha_emision"]
            invoice_client = df.at[0, "cliente"]
            invoice_total = df.at[0, "total"]
        else:
            invoice_date = invoice_client = invoice_total = "N/A"

        # Aquí puedes obtener y mostrar los detalles de la factura
        # Por ejemplo, mostrar un QMessageBox con los detalles
        msgbox = MsgBoxFactory()
        msg = msgbox.create_msg_box(
            "information",
            "Detalles de la Factura",(
            f"<h3>Detalles de la Factura</h3>"
            f"<p><b>ID:</b> {invoice_id}</p>"
            f"<p><b>Fecha:</b> {invoice_date}</p>"
            f"<p><b>Cliente:</b> {invoice_client}</p>"
            f"<p><b>Total:</b> ${float(invoice_total):.2f}</p>"),
            QMessageBox.NoIcon, "Archivo Medium", 12, "Volver", QMessageBox.AcceptRole
        )
        msg.exec()

    def export(self):
        Export().export_data("invoices")
    
    def open_settings(self):
        from settings import SettingsWindow
        self.settings_window = SettingsWindow()
        self.settings_window.show()
