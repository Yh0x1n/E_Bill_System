"""Módulo de generación de facturas"""
from PySide6.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QSizePolicy, QComboBox, QTableWidget, QTableWidgetItem, QHeaderView, QCheckBox, QHBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from datetime import datetime, date
from clients import Client
from products import Product
from service import s
from styles.labels import LabelFactory
from styles.buttons import ButtonFactory
import random, os, sys, pandas as pd

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

        self.invoice_label = label.create_label("Factura", "Archivo Black", "bold_black", 32)
        self.headerLayout.addWidget(self.invoice_label, 0, 0, 1, 3, Qt.AlignLeft | Qt.AlignTop)

        self.invoice_sublabel = label.create_label("Genera tus facturas fácil y rápido", "Archivo Black", "bold_black", 16)
        self.headerLayout.addWidget(self.invoice_sublabel, 1, 0, 1, 3, Qt.AlignLeft | Qt.AlignTop)

        self.invoiceLayout.addLayout(self.headerLayout)

    def initButtons(self):
        button = ButtonFactory()

        self.btn_settings = button.create_button("", "default_black", "src/assets/icons/settings.png", min_size = (75, 75))
        self.headerLayout.addWidget(self.btn_settings, 0, 3, Qt.AlignTop | Qt.AlignRight)

        self.btn_add_client = button.create_button("", "default_black", "src/assets/icons/add_client.png", min_size=(75, 75))
        self.btn_add_client.clicked.connect(Client().add_client)
        self.fieldsLayout.addWidget(self.btn_add_client, 1, 1, Qt.AlignLeft)

        self.btn_add_product = button.create_button("", "default_black", "src/assets/icons/add_product.png", min_size=(75, 75))
        self.btn_add_product.clicked.connect(Product().add_product)
        self.fieldsLayout.addWidget(self.btn_add_product, 1, 2, Qt.AlignLeft)

        self.btn_update_lists = button.create_button("", "default_black", "src/assets/icons/update.png", min_size=(75, 75))
        self.btn_update_lists.clicked.connect(self.update_lists)
        self.fieldsLayout.addWidget(self.btn_update_lists, 1, 3, Qt.AlignLeft)

        self.btn_generate_invoice = button.create_button("Generar", "accept", None, 12, (75, 35))
        self.btn_generate_invoice.clicked.connect(self.generate_invoice)
        self.fieldsLayout.addWidget(self.btn_generate_invoice, 4, 0, Qt.AlignLeft)

        descriptions = ["Agregar cliente", "Agregar producto", "Actualizar listas"]
        buttons = [self.btn_add_client, self.btn_add_product, self.btn_update_lists]

        for i, button in enumerate(buttons):
            button.setToolTip(descriptions[i])

    def initFields(self):
        from service import s
        label = LabelFactory()

        self.fieldsLayout = QGridLayout()
        self.fieldsLayout.setContentsMargins(0, 0, 0, 0)
        self.fieldsLayout.setSpacing(10)
        self.fieldsLayout.setColumnStretch(0, 2)

        #Combobox de cliente
        self.client_combobox = QComboBox()
        self.client_combobox.setPlaceholderText("Seleccione un cliente")  # Texto placeholder

        clients = s.get_client_by_id()  # Obtener lista de clientes desde la base de datos
        for client in clients:
            self.client_combobox.addItem(f"{client[0]} - {client[1]}")  # Mostrar ID y nombre en el desplegable
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

        #Agregar labels que al seleccionar un cliente de la ComboBox se muestren los datos extrayéndolos directamente de la base de datos
        # Labels para mostrar datos del cliente seleccionado
        self.client_info_label = label.create_label("Información del Cliente", "Archivo Medium", "medium_black", 12)
        self.fieldsLayout.addWidget(self.client_info_label, 2, 0, Qt.AlignLeft)

        self.client_details_label = label.create_label("", "Archivo Medium", "medium_black", 12)
        self.fieldsLayout.addWidget(self.client_details_label, 3, 0, Qt.AlignLeft)

        # Conectar la selección de la combobox con la actualización de los labels
        def update_client_details(index):
            if index >= 0:
                client_id = self.client_combobox.currentText().split(" - ")[0]
                query = f"SELECT id_cliente, nombre_cliente, email FROM cliente WHERE id_cliente = '{client_id}';"
                client_data = s.cur.execute(query).fetchone()
                self.client_details_label.setText(f"ID: {client_data[0]}        Nombre: {client_data[1]}"
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
        
        # Fetch data from the database
        df = pd.read_sql("SELECT id_producto, nombre, precio FROM producto;", s.conn)

        # Crear y configurar la tabla
        self.product_table = QTableWidget()
        self.product_table.setRowCount(len(df))
        self.product_table.setColumnCount(len(df.columns) + 1)  # Add an extra column for checkboxes
        self.product_table.setHorizontalHeaderLabels(["N°", "Nombre", "Precio", "Seleccionar"])
        self.product_table.setMinimumSize(600, 200)
        self.product_table.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.product_table.setFont(QFont("Archivo Medium", 12))
        self.product_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.product_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.product_table.setSelectionMode(QTableWidget.SingleSelection)
        self.product_table.setStyleSheet("""QTableWidget::item:selected {
                                                                        background-color: #0078d7;
                                                                        color: white;
                                                                    }
                                                                    QTableWidget::item:hover {
                                                                        background-color: #f0f0f0;
                                                                        color: black;
                                                                    }
                                                                    QTableWidget::item {
                                                                        padding: 10px;
                                                                    }
                                                                    QTableWidget {
                                                                        border: 1px solid #d0d0d0;
                                                                        border-radius: 5px;
                                                                        background-color: white;
                                                                        color: black;
                                                                        padding: 5px;
                                                                    }""")
        for i in range(self.product_table.rowCount()):
            self.product_table.setRowHeight(i, 40)

        # Function to update the total amount
        def update_total_amount():
            total = 0
            for i in range(self.product_table.rowCount()):
                cell_widget = self.product_table.cellWidget(i, 3)
                if cell_widget and cell_widget.findChild(QCheckBox).isChecked():
                    price_str = self.product_table.item(i, 2).text().replace('$', '')
                    total += float(price_str)
            self.total_amount_label.setText(f"Total: ${total:.2f}")

        # Llenar la tabla con datos y agregar checkboxes
        for i, row in df.iterrows():
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                self.product_table.setItem(i, j, item)

            # Crear y agregar el checkbox
            checkbox = QCheckBox()
            checkbox.stateChanged.connect(update_total_amount)

            #Crear el widget para el checkbox
            cell_widget = QWidget()
            cell_layout = QHBoxLayout(cell_widget)
            cell_layout.setAlignment(Qt.AlignCenter)
            cell_layout.setContentsMargins(0, 0, 0, 0)
            cell_layout.addWidget(checkbox)
            self.product_table.setCellWidget(i, 3, cell_widget)
        
        self.product_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        def handle_table_click(row, col):
            if col == 3:
                cell_widget = self.product_table.cellWidget(row, col)
                if cell_widget:
                    checkbox = cell_widget.findChild(QCheckBox)
                    if checkbox:
                        checkbox.setChecked(not checkbox.isChecked())

        self.product_table.cellClicked.connect(handle_table_click)

        # Formatear el precio con un signo de dólar
        for i in range(self.product_table.rowCount()):
            price_item = self.product_table.item(i, 2)
            if price_item:
                price_item.setText(f"${price_item.text()}")
        
        # Perform initial total calculation
        update_total_amount()

        self.invoiceLayout.addLayout(self.listLayout)
        self.listLayout.addWidget(self.product_table)
    
    def update_lists(self): #Método que actualiza la combobox y la lista
        from service import s

        # Actualizar la combobox de clientes
        self.client_combobox.clear()
        clients = s.get_client_by_id()
        for client in clients:
            self.client_combobox.addItem(f"{client[0]} - {client[1]}")
        
        # Actualizar la tabla de productos
        df = pd.read_sql("SELECT id_producto, nombre, precio FROM producto;", s.conn)
        self.product_table.setRowCount(len(df))
        for i, row in df.iterrows():
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                self.product_table.setItem(i, j, item)

        for i in range(self.product_table.rowCount()):
            price_item = self.product_table.item(i, 2)
            if price_item:
                # Evitamos agregar doble dólar si ya lo contiene
                if not price_item.text().startswith("$"):
                    price_item.setText(f"${price_item.text()}")

    def generate_invoice(self):
        from invoice_lib.templates import SimpleInvoice
        from invoice_lib.models import ServiceProviderInfo, ClientInfo, InvoiceInfo, Item

        now = datetime.now()

        # Obtener datos del cliente y los productos seleccionados
        client_id = self.client_combobox.currentText().split(" - ")[0]
        product_ids = [self.product_table.item(i, 0).text() for i in range(self.product_table.rowCount()) if self.product_table.cellWidget(i, 3).findChild(QCheckBox).isChecked()]
        query = f"SELECT id_cliente, nombre_cliente, email FROM cliente WHERE id_cliente = '{client_id}';"
        query2 = f"SELECT id_producto, nombre, precio FROM producto WHERE id_producto IN ({', '.join(['?' for _ in product_ids])});"
        
        client_data = s.cur.execute(query).fetchone()
        product_data = s.cur.execute(query2, product_ids).fetchall()

        invoice_id = f"INV-{random.randint(100, 999)}"
        invoice_datetime = now.strftime("%d/%m/%Y")
        due_datetime = now.strftime("%d/%m/%Y")

        #Agregar la información del cliente y el proveedor de servicios
        doc = SimpleInvoice(f"{invoice_id}.pdf")
        doc.invoice_info = InvoiceInfo(invoice_id=invoice_id, invoice_datetime=invoice_datetime, due_datetime=due_datetime)
        
        for product in product_data:
            doc.add_item(Item(product[1], "Descripción del producto", 1, float(product[2])))
        
    
        doc.client_info = ClientInfo(name=client_data[1], street="Dirección del cliente", city="Ciudad", state="Estado", email=client_data[2], client_id=client_data[0])
        
        doc.service_provider_info = ServiceProviderInfo(name="Nombre del proveedor", street="Dirección del proveedor", city="Ciudad", state="Estado", vat_tax_number="Número de IVA", email="Email del proveedor", phone="Teléfono del proveedor")

        tax = 20
        doc.set_item_tax_rate(tax)

        doc.set_bottom_tip("Gracias por su compra!")

        doc.finish()