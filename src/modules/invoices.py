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
from styles.lists import apply_table_style

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

        self.btn_generate_invoice = button.create_button("Generar", "accept", None, 12, (100, 35))
        self.btn_generate_invoice.clicked.connect(self.generate_invoice)
        self.fieldsLayout.addWidget(self.btn_generate_invoice, 5, 1, 1, 4, Qt.AlignRight)

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
        self.product_table.setColumnCount(len(df.columns) + 2)  # Add two extra columns for units counter and checkboxes
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
        
        # Llenar la tabla con datos y agregar checkboxes
        for i, row in df.iterrows():
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                self.product_table.setItem(i, j, item)

            # Crear y agregar el checkbox
            checkbox = QCheckBox()
            checkbox.stateChanged.connect(self.update_total_amount)

            #Crear el widget para el checkbox
            checkbox_cell_widget = QWidget()
            checkbox_cell_layout = QHBoxLayout(checkbox_cell_widget)
            checkbox_cell_layout.setAlignment(Qt.AlignCenter)
            checkbox_cell_layout.setContentsMargins(0, 0, 0, 0)
            checkbox_cell_layout.addWidget(checkbox)
            self.product_table.setCellWidget(i, 4, checkbox_cell_widget)

            #Crear el widget para los botones + y - del contador
            counter_cell_widget = QWidget()
            counter_cell_layout = QHBoxLayout(counter_cell_widget)   
            counter_cell_layout.setAlignment(Qt.AlignCenter)
            counter_cell_layout.setContentsMargins(0, 0, 0, 0)
            
            # Crear nuevos botones y etiqueta para cada fila
            btn_minus = ButtonFactory().create_button("-", "default_black", None, min_size=(10, 10))
            btn_plus = ButtonFactory().create_button("+", "default_black", None, min_size=(10, 10))
            unit_label = l.create_label("1", "Archivo Medium", "medium_black", 12)
            
            # Conectar los botones a funciones que actualicen unit_label (cada función debe saber a qué etiqueta modificar)
            btn_minus.clicked.connect(lambda _, lbl=unit_label: (lbl.setText(str(max(0, int(lbl.text()) - 1))), self.update_total_amount()))
            btn_plus.clicked.connect(lambda _, lbl=unit_label: (lbl.setText(str(int(lbl.text()) + 1)), self.update_total_amount()))
            
            counter_cell_layout.addWidget(btn_minus)
            counter_cell_layout.addWidget(unit_label)
            counter_cell_layout.addWidget(btn_plus)
            self.product_table.setCellWidget(i, 3, counter_cell_widget)
        
            self.product_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.product_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
            #self.product_table.horizontalHeader().setStretchLastSection(True)

        def handle_table_click(row, col):
            if col == 4:
                checkbox_cell_widget = self.product_table.cellWidget(row, col)
                if checkbox_cell_widget:
                    checkbox = checkbox_cell_widget.findChild(QCheckBox)
                    if checkbox:
                        checkbox.setChecked(not checkbox.isChecked())

        self.product_table.cellClicked.connect(handle_table_click)

        # Formatear el precio con un signo de dólar
        for i in range(self.product_table.rowCount()):
            price_item = self.product_table.item(i, 2)
            if price_item:
                price_item.setText(f"${price_item.text()}")
        
        # Perform initial total calculation
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

        # Actualizar la combobox de clientes
        self.client_combobox.clear()
        clients = s.get_client_by_id()
        for client in clients:
            self.client_combobox.addItem(f"{client[0]} - {client[1]}")
        
        # Actualizar la tabla de productos
        df = pd.read_sql("SELECT id_producto, nombre, precio FROM producto;", s.conn)
        self.product_table.setRowCount(len(df))

        for i in range(self.product_table.rowCount()):
            self.product_table.setRowHeight(i, 40)

        for i, row in df.iterrows():
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
            
            # Crear nuevos botones y etiqueta para cada fila
            btn_minus = ButtonFactory().create_button("-", "default_black", None, min_size=(10, 10))
            btn_plus = ButtonFactory().create_button("+", "default_black", None, min_size=(10, 10))
            unit_label = l.create_label("1", "Archivo Medium", "medium_black", 12)
            
            # Conectar los botones a funciones que actualicen unit_label (cada función debe saber a qué etiqueta modificar)
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
        from invoice_lib.templates import SimpleInvoice
        from invoice_lib.models import ServiceProviderInfo, ClientInfo, InvoiceInfo, Item

        now = datetime.now()

        # Obtener datos del cliente y los productos seleccionados
        client_id = self.client_combobox.currentText().split(" - ")[0]
        product_ids = [self.product_table.item(i, 0).text() for i in range(self.product_table.rowCount()) if self.product_table.cellWidget(i, 4).findChild(QCheckBox).isChecked()]
        query = f"SELECT id_cliente, nombre_cliente, email, direccion, telefono, cedula FROM cliente WHERE id_cliente = '{client_id}';"
        query2 = f"SELECT id_producto, nombre, precio, descripcion FROM producto WHERE id_producto IN ({', '.join(['?' for _ in product_ids])});"
        
        client_data = s.cur.execute(query).fetchone()
        product_data = s.cur.execute(query2, product_ids).fetchall()

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
        
        doc.client_info = ClientInfo(name=client_data[1], street=client_data[3], phone=client_data[4] , email=client_data[2], client_id=client_data[0], vat_tax_number=client_data[5])
        
        doc.service_provider_info = ServiceProviderInfo(name="Nombre del proveedor", street="Dirección del proveedor", city="Ciudad", state="Estado", vat_tax_number="Número de IVA", email="Email del proveedor", phone="Teléfono del proveedor")

        tax = 5
        doc.set_item_tax_rate(tax)

        doc.set_bottom_tip("Gracias por su compra!")

        doc.finish()