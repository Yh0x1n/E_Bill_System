"""
Módulo de gestión de clientes
"""

from PySide6.QtWidgets import QWidget, QMainWindow, QVBoxLayout, QGridLayout, QTableWidget, QSizePolicy, QTableWidgetItem, QHeaderView, QLineEdit, QMessageBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from styles.labels import LabelFactory
from styles.buttons import ButtonFactory

class Client(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.clientLayout = QVBoxLayout(self)
        self.clientLayout.setContentsMargins(10, 10, 10, 10)
        self.clientLayout.setSpacing(5)
        
        self.initUI()
        
    def initUI(self): #Inicio de la interfaz gráfica
        self.initHeader()
        self.initButtons()
        self.initList()
        
    def initHeader(self): #Inicio del header
        label = LabelFactory()

        self.headerLayout = QGridLayout()  # Cambiar a QGridLayout para organizar el header
        self.client_label = label.create_label("Clientes", "Archivo Black", "bold_black", 32)
        self.headerLayout.addWidget(self.client_label, 0, 0, 1, 3, Qt.AlignLeft)

        self.client_sublabel = label.create_label("Administra tus clientes", "Archivo Black", "bold_black", 16)
        self.headerLayout.addWidget(self.client_sublabel, 1, 0, 1, 3, Qt.AlignLeft)

        self.clientLayout.addLayout(self.headerLayout)  # Añadir el headerLayout al layout principal

    def initButtons(self): #Inicio de los botones
        button = ButtonFactory()

        self.buttonLayout = QGridLayout()
        self.buttonLayout.setContentsMargins(0, 100, 0, 0)
        self.buttonLayout.setSpacing(5)
        self.buttonLayout.setAlignment(Qt.AlignBottom)
        self.clientLayout.addLayout(self.buttonLayout)

        self.btn_settings = button.create_button("", "default_black", "src/assets/icons/settings.png", min_size = (75, 75))
        self.headerLayout.addWidget(self.btn_settings, 0, 3, 2, 2, Qt.AlignTop | Qt.AlignRight)
        
        self.btn_add = button.create_button("", "default_black", "src/assets/icons/Icon.png", min_size = (75, 75))
        self.btn_add.clicked.connect(self.add_client)
        self.buttonLayout.addWidget(self.btn_add, 4, 3, 3, 4, Qt.AlignBottom | Qt.AlignRight)

        self.btn_edit = button.create_button("", "default_black", "src/assets/icons/Pen.png", min_size = (75, 75))
        self.btn_edit.clicked.connect(self.edit_client)
        self.buttonLayout.addWidget(self.btn_edit, 4, 4, 3, 4, Qt.AlignBottom | Qt.AlignRight)

        self.btn_delete = button.create_button("", "default_black", "src/assets/icons/Trash.png", min_size = (75, 75))
        self.btn_delete.clicked.connect(self.delete_client)
        self.buttonLayout.addWidget(self.btn_delete, 4, 5, 3, 4, Qt.AlignBottom | Qt.AlignRight)

        description = ["Editar", "Agregar", "Eliminar", "Ajustes"]
        buttons = [self.btn_edit, self.btn_add, self.btn_delete, self.btn_settings]
        
        for i, button in enumerate(buttons):
            button.setToolTip(description[i])

    def initList(self): #Inicio de la lista de clientes
        import pandas as pd
        from service import s

        self.listLayout = QVBoxLayout()
        self.listLayout.setAlignment(Qt.AlignBottom)
        self.listLayout.setContentsMargins(0, 0, 0, 0)
        self.clientLayout.addLayout(self.listLayout)

        # Fetch data from the database
        df = pd.read_sql("SELECT id_cliente, nombre_cliente, telefono, email FROM cliente;", s.conn)

        # Crear y configurar la tabla
        self.client_table = QTableWidget()
        self.client_table.setRowCount(len(df))
        self.client_table.setColumnCount(len(df.columns))
        self.client_table.setHorizontalHeaderLabels(["N°", "Nombre", "Teléfono", "Email"])
        self.client_table.setMinimumSize(600, 200)
        self.client_table.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.client_table.setFont(QFont("Archivo Medium", 12))
        self.client_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.client_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.client_table.setSelectionMode(QTableWidget.SingleSelection)
        self.client_table.setStyleSheet("""QTableWidget::item:selected {
                                                                        background-color: #0078d7;
                                                                        color: white;
                                                                    }
                                                                    QTableWidget::item:hover {
                                                                        background-color: #f0f0f0;
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

        # Llenar la tabla con datos
        for i, row in df.iterrows():
            for j, value in enumerate(row):
                self.client_table.setItem(i, j, QTableWidgetItem(str(value)))

        self.client_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.listLayout.addWidget(self.client_table)
        self.client_table.itemDoubleClicked.connect(lambda _: self.show_details())
        self.client_table.itemActivated.connect(lambda _: self.show_details())
    
    def add_client(self):
        label = LabelFactory()
        button = ButtonFactory()

        input_stylesheet = ("""
                        color: black;
                        background-color: white;
                        border: 1px solid black;
                        border-radius: 5px;
                        font-family: "Archivo Medium";
                        font-size: 16px;
                        padding: 5px;
                        """)

        self.w = QMainWindow()
        self.w.setFixedSize(640, 400)
        self.w.setWindowTitle("Lanchmann - Agregar cliente")
        self.w.setStyleSheet("""background-color: white;""")
        self.w.setContentsMargins(20,20,20,20)
        
        central_widget = QWidget(self.w)
        central_widget.setContentsMargins(10, 10, 10, 10)
        central_widget.setStyleSheet("background-color: #f0f0f0; border-radius: 20px;")
        self.w.setCentralWidget(central_widget)

        self.w_layout = QGridLayout()
        self.w_layout.setContentsMargins(5, 5, 5, 5)
        self.w_layout.setSpacing(5)
        central_widget.setLayout(self.w_layout)

        # Header label for the "Agregar Cliente" section
        header_label = label.create_label("Agregar Cliente", "Archivo Medium", "medium_black", 20)
        header_sublabel = label.create_label("Completa los campos necesarios para\nañadir a tu cliente", "Archivo Medium", "medium_black", 14)
        self.w_layout.addWidget(header_label, 0, 0, Qt.AlignLeft)
        self.w_layout.addWidget(header_sublabel, 1, 0, Qt.AlignLeft | Qt.AlignTop)

        #Campos de texto y botones
        fields = [
            ("nombre", "Nombre del cliente"),
            ("cedula", "Cédula de Id."),
            ("dir", "Dirección"),
            ("tlf", "Teléfono"),
            ("email", "Correo electrónico")
        ]
        buttons = [("accept", "Aceptar"), ("cancel", "Cancelar")]
        # Definir la función command antes de conectar señales
        def command():
            from service import s
            import pandas as pd
            from styles.msg_boxes import MsgBoxFactory

            # Obtener los valores de cada campo
            fields_values = [
            ('nombre', self.nombre_input),
            ('cedula', self.cedula_input),
            ('direccion', self.dir_input),
            ('telefono', self.tlf_input),
            ('email', self.email_input)
            ]
            values = [field.text() for _, field in fields_values]
            if any(val.strip() == "" for val in values):
                print("No se puede introducir un campo vacío.")
            else:
                try:
                    msgbox = MsgBoxFactory()
                    
                    q = msgbox.create_question_box("question", "Información", "¿Deseas añadir este cliente?", QMessageBox.Question, "Archivo Medium", 12, ["Sí", "No"], [QMessageBox.AcceptRole, QMessageBox.RejectRole])
                    q.exec()

                    if q.clickedButton().text() == "Sí":
                        q2 = msgbox.create_msg_box("information", "Información", "Cliente agregado correctamente", QMessageBox.Information, "Archivo Medium", 12, "Aceptar", QMessageBox.AcceptRole)
                        q2.exec()

                        s.insert_client(*values)
                        
                        self.w.close()

                    # Refrescar la tabla con los nuevos datos
                    df = pd.read_sql("SELECT id_cliente, nombre_cliente, telefono, email FROM cliente;", s.conn)
                    self.client_table.setRowCount(len(df))
                    for i, row in df.iterrows():
                        for j, value in enumerate(row):
                            self.client_table.setItem(i, j, QTableWidgetItem(str(value)))

                except Exception as e:
                    print("Error al insertar el cliente:", e)
        def close():
            self.w.close()

        # Agregar QLineEdit para cada campo usando el texto como placeholder
        for i, (key, text) in enumerate(fields):
            row = ((i // 2) * 2) + 2  # Empezar en la fila 1, luego filas 1-2, 3-4, etc.
            col = i % 2

            field_input = QLineEdit()
            field_input.setStyleSheet(input_stylesheet)
            field_input.setPlaceholderText(text)

            if key == "dir":
                field_input.setMinimumWidth(275)
            elif key == "email":
                field_input.setMinimumWidth(250)
            elif key == "nombre":
                field_input.setMinimumWidth(200)

            setattr(self, f"{key}_input", field_input)
            self.w_layout.addWidget(getattr(self, f"{key}_input"), row, col, Qt.AlignLeft)

            # Conectar la tecla Enter para ejecutar command en cada campo
            field_input.returnPressed.connect(command)

        for i, (key, text) in enumerate(buttons):
            col = i % 2
            style = "accept" if key == "accept" else "cancel"
            setattr(self, f'btn_{key}', button.create_button(text, style, None, 16, (125, 50)))
            self.w_layout.addWidget(getattr(self, f'btn_{key}'), 7, col, Qt.AlignCenter)

        # Vincular la función command al botón "Aceptar"
        self.btn_accept.clicked.connect(command)
        self.btn_cancel.clicked.connect(close)

        self.w.show()

    def edit_client(self): #Método para editar los clientes 
        from service import s

        label = LabelFactory()
        button = ButtonFactory()

        input_stylesheet = ("""
                        color: black;
                        background-color: white;
                        border: 1px solid black;
                        border-radius: 5px;
                        font-family: "Archivo Medium";
                        font-size: 16px;
                        padding: 5px;
                        """)

        self.w = QMainWindow()
        self.w.setFixedSize(640, 400)
        self.w.setWindowTitle("Lanchmann - Agregar cliente")
        self.w.setStyleSheet("""background-color: white;""")
        self.w.setContentsMargins(20,20,20,20)
        
        central_widget = QWidget(self.w)
        central_widget.setContentsMargins(10, 10, 10, 10)
        central_widget.setStyleSheet("background-color: #f0f0f0; border-radius: 20px;")
        self.w.setCentralWidget(central_widget)

        self.w_layout = QGridLayout()
        self.w_layout.setContentsMargins(5, 5, 5, 5)
        self.w_layout.setSpacing(5)
        central_widget.setLayout(self.w_layout)

        # Header label for the "Agregar Cliente" section
        header_label = label.create_label("Editar cliente", "Archivo Medium", "medium_black", 20)
        header_sublabel = label.create_label("Especifica los campos que desees editar", "Archivo Medium", "medium_black", 14)
        self.w_layout.addWidget(header_label, 0, 0, Qt.AlignLeft)
        self.w_layout.addWidget(header_sublabel, 1, 0, Qt.AlignLeft | Qt.AlignTop)

        #Campos de texto y botones
        row = self.client_table.currentRow()
        client_id = self.client_table.item(row, 0).text()
        
        client_details = s.show_client_details(client_id)
        if client_details:
            details = client_details[0]  # Assumes the result is a tuple: (id, nombre, cedula, dirección, teléfono, email)
            cedula = details[2]
            direccion = details[3]
        else:
            cedula = ""
            direccion = ""
        
        fields = [
            ("nombre", f"{self.client_table.item(row, 1).text()}"),
            ("cedula", cedula),
            ("dir", direccion),
            ("tlf", f"{self.client_table.item(row, 2).text()}"),
            ("email", f"{self.client_table.item(row, 3).text()}")
        ]

        buttons = [("accept", "Aceptar"), ("cancel", "Cancelar")]

        def command():
            from service import s
            import pandas as pd
            from styles.msg_boxes import MsgBoxFactory

            # Obtener los valores de cada campo
            fields_values = [
            ('nombre', self.nombre_input),
            ('cedula', self.cedula_input),
            ('direccion', self.dir_input),
            ('telefono', self.tlf_input),
            ('email', self.email_input)
            ]

            values = [field.text() for _, field in fields_values]
            
            try:
                msgbox = MsgBoxFactory()
                
                q = msgbox.create_question_box("question", "Información", "¿Deseas guardar los cambios?", QMessageBox.Question, "Archivo Medium", 12, ["Sí", "No"], [QMessageBox.AcceptRole, QMessageBox.RejectRole])
                q.exec()

                if q.clickedButton().text() == "Sí":
                    q2 = msgbox.create_msg_box("information", "Información", "Cliente editado correctamente", QMessageBox.Information, "Archivo Medium", 12, "Aceptar", QMessageBox.AcceptRole)
                    q2.exec()

                    s.insert_client(*values)
                    
                    self.w.close()

                # Refrescar la tabla con los nuevos datos
                df = pd.read_sql("SELECT id_cliente, nombre_cliente, telefono, email FROM cliente;", s.conn)
                self.client_table.setRowCount(len(df))
                for i, row in df.iterrows():
                    for j, value in enumerate(row):
                        self.client_table.setItem(i, j, QTableWidgetItem(str(value)))

            except Exception as e:
                print("Error al editar el cliente:", e)

        def close():
            self.w.close()

        for i, (key, text) in enumerate(fields):
            row = ((i // 2) * 2) + 2  # Empezar en la fila 1, luego filas 1-2, 3-4, etc.
            col = i % 2

            field_input = QLineEdit()
            field_input.setStyleSheet(input_stylesheet)
            field_input.setPlaceholderText(text)

            match key:
                case "dir":
                    field_input.setMinimumWidth(275)
                case "email":
                    field_input.setMinimumWidth(250)
                case "nombre":
                    field_input.setMinimumWidth(200)
                case _:
                    pass

            setattr(self, f"{key}_input", field_input)
            self.w_layout.addWidget(getattr(self, f"{key}_input"), row, col, Qt.AlignLeft)

            # Conectar la tecla Enter para ejecutar command en cada campo
            field_input.returnPressed.connect(command)

        for i, (key, text) in enumerate(buttons):
            col = i % 2
            style = "accept" if key == "accept" else "cancel"
            setattr(self, f'btn_{key}', button.create_button(text, style, None, 16, (125, 50)))
            self.w_layout.addWidget(getattr(self, f'btn_{key}'), 7, col, Qt.AlignCenter)

        # Vincular la función command al botón "Aceptar"
        self.btn_accept.clicked.connect(command)
        self.btn_cancel.clicked.connect(close)

        self.w.show()
    
    def delete_client(self): #Método para borrar un cliente
        from service import s
        from PySide6.QtWidgets import QMessageBox
        
        # Verificar que se haya seleccionado un cliente
        selected_items = self.client_table.selectedItems()
        if not selected_items:
            QMessageBox.information(self, "Información", "Seleccione un cliente a eliminar.")
            return
        
        # Extraer el ID del cliente (asumiendo que está en la primera columna)
        row = selected_items[0].row()
        client_id_item = self.client_table.item(row, 0)
        client_id = client_id_item.text()
        
        try:
            s.delete_client(client_id)
            QMessageBox.information(self, "Información", "Cliente eliminado correctamente.")
            self.client_table.removeRow(row)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo eliminar el cliente: {e}")

    def show_details(self):
        from service import s
        
        label = LabelFactory()
        button = ButtonFactory()

        selected_items = self.client_table.selectedItems()
        if not selected_items:
            return

        # Obtener el ID del cliente de la primera columna
        row = selected_items[0].row()
        client_id = self.client_table.item(row, 0).text()

        # Consultar detalles del cliente en la base de datos
        client_details = s.show_client_details(client_id)
        if not client_details:
            return

        # Crear un QWidget para mostrar los detalles
        self.detail_window = QMainWindow(self)
        self.detail_window.setFixedSize(675,250)
        self.detail_window.setWindowModality(Qt.WindowModal)
        self.detail_window.setWindowFlags(Qt.WindowCloseButtonHint | Qt.Tool)
        self.detail_window.setWindowTitle("Detalles del Cliente")
        self.detail_window.setStyleSheet("background-color: white;")

        self.central_widget = QWidget()

        self.detail_layout = QGridLayout()
        self.detail_layout.setContentsMargins(10, 10, 10, 10)
        self.central_widget.setLayout(self.detail_layout)
        self.detail_window.setCentralWidget(self.central_widget)

        # Mostrar los detalles del cliente
        labels = ["ID Cliente", "Nombre", "Cédula de Id.", "Dirección", "Teléfono", "Email"]
        positions = [(i+1, j) for i in range(6) for j in range(2)]

        title_label = label.create_label("Detalles del Cliente", "Archivo Black", "bold_black", 18)
        self.detail_layout.addWidget(title_label, 0, 0, Qt.AlignLeft)

        for i, detail in enumerate(client_details[0]):
            detail_label = label.create_label(f"{labels[i]}: {detail}", "Archivo Medium", "medium_black", 14)
            if labels[i] == "Dirección":
                detail_label.setFixedSize(300, 65)
                detail_label.setAlignment(Qt.AlignLeft)
                detail_label.setWordWrap(True)
            self.detail_layout.addWidget(detail_label, positions[i][0], positions[i][1], Qt.AlignLeft)

        accept_button = button.create_button("Volver", "accept", None, 16, (100, 50))
        accept_button.clicked.connect(self.detail_window.close)
        self.detail_layout.addWidget(accept_button, 5, 1, Qt.AlignCenter | Qt.AlignRight)

        self.detail_window.show()