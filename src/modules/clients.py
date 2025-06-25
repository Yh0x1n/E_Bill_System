"""
Módulo de gestión de clientes
"""

from PySide6.QtWidgets import QWidget, QMainWindow, QVBoxLayout, QGridLayout, QTableWidget, QSizePolicy, QTableWidgetItem, QHeaderView, QLineEdit, QMessageBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QIcon
from styles.labels import LabelFactory
from styles.buttons import ButtonFactory
from styles.msg_boxes import MsgBoxFactory
from styles.lists import apply_table_style
from export import Export
from service import s
from resource_util import resource_path
import polars as pl
import os.path


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
        self.btn_settings = button.create_button("", "default_black", resource_path("assets/icons/settings.png"), min_size = (75, 75))
        self.headerLayout.addWidget(self.btn_settings, 0, 3, 2, 2, Qt.AlignTop | Qt.AlignRight)
        self.btn_add = button.create_button("", "default_black", resource_path("assets/icons/Icon.png"), min_size = (75, 75))
        self.btn_add.clicked.connect(self.add_client)
        self.buttonLayout.addWidget(self.btn_add, 4, 3, 3, 4, Qt.AlignBottom | Qt.AlignRight)
        self.btn_edit = button.create_button("", "default_black", resource_path("assets/icons/Pen.png"), min_size = (75, 75))
        self.btn_edit.clicked.connect(self.edit_client)
        self.buttonLayout.addWidget(self.btn_edit, 4, 4, 3, 4, Qt.AlignBottom | Qt.AlignRight)
        self.btn_delete = button.create_button("", "default_black", resource_path("assets/icons/Trash.png"), min_size = (75, 75))
        self.btn_delete.clicked.connect(self.delete_client)
        self.buttonLayout.addWidget(self.btn_delete, 4, 5, 3, 4, Qt.AlignBottom | Qt.AlignRight)
        self.btn_export = button.create_button("", "default_black", resource_path("assets/icons/excel.png"), min_size=(75, 75))
        self.btn_export.clicked.connect(self.export)
        self.buttonLayout.addWidget(self.btn_export, 4, 6, 3, 4, Qt.AlignBottom | Qt.AlignRight)
        description = ["Editar", "Agregar", "Eliminar", "Ajustes", "Exportar a Excel"]
        buttons = [self.btn_edit, self.btn_add, self.btn_delete, self.btn_settings, self.btn_export]
        for i, button in enumerate(buttons):
            button.setToolTip(description[i])

    def initList(self): #Inicio de la lista de clientes
        self.listLayout = QVBoxLayout()
        self.listLayout.setAlignment(Qt.AlignBottom)
        self.listLayout.setContentsMargins(0, 0, 0, 0)
        self.clientLayout.addLayout(self.listLayout)

        # Fetch data from the database usando Polars
        df = pl.read_database("SELECT id_cliente, nombre_cliente, telefono, email FROM cliente;", s.conn)

        # Crear y configurar la tabla
        self.client_table = QTableWidget()
        self.client_table.setRowCount(df.height)
        self.client_table.setColumnCount(len(df.columns))
        self.client_table.setHorizontalHeaderLabels(["N°", "Nombre", "Teléfono", "Email"])
        self.client_table.setMinimumSize(600, 200)
        self.client_table.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.client_table.setFont(QFont("Archivo Medium", 12))
        self.client_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.client_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.client_table.setSelectionMode(QTableWidget.SingleSelection)

        # Llenar la tabla con datos usando Polars
        for i, row in enumerate(df.iter_rows()):
            for j, value in enumerate(row):
                self.client_table.setItem(i, j, QTableWidgetItem(str(value)))

        self.client_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.listLayout.addWidget(self.client_table)
        self.client_table.itemDoubleClicked.connect(lambda _: self.show_details())
        self.client_table.keyPressEvent = self._client_table_key_press_event

        # Apply styles to the client table
        apply_table_style(self.client_table)

    def _client_table_key_press_event(self, event):
        if event.key() == Qt.Key_Delete:
            self.delete_client()
        else:
            super(QTableWidget, self.client_table).keyPressEvent(event)

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
        self.w.setWindowIcon(QIcon(resource_path("assets/pictures/AqualabLogo.jpg")))
        self.w.setStyleSheet("""background-color: white;""")
        self.w.setContentsMargins(20,20,20,20)
        self.w.setWindowFlags(Qt.WindowCloseButtonHint)
        
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
            ("cedula", "Cédula/NIT"),
            ("dir", "Dirección"),
            ("tlf", "Teléfono"),
            ("email", "Correo electrónico"),
            ("fiscal_regime", "Régimen Fiscal (opcional)"),
            ("tax_responsibility", "Responsabilidad Tributaria (opcional)"),
            ("economic_activity", "Actividad Económica (opcional)")
        ]
        buttons = [("accept", "Aceptar"), ("cancel", "Cancelar")]
        # Definir la función command antes de conectar señales
        def command():
            from service import s
            # Obtener los valores de cada campo
            fields_values = [
                ('nombre', self.nombre_input),
                ('cedula', self.cedula_input),
                ('direccion', self.dir_input),
                ('telefono', self.tlf_input),
                ('email', self.email_input),
                ('fiscal_regime', self.fiscal_regime_input),
                ('tax_responsibility', self.tax_responsibility_input),
                ('economic_activity', self.economic_activity_input)
            ]
            values = [field.text() if field.text().strip() != '' else None for _, field in fields_values]
            if any(val is None for val in values[:5]):
                msgbox = MsgBoxFactory()
                msgbox.create_msg_box("error", "Error", "Por favor, completa todos los campos obligatorios.", QMessageBox.Critical, "Archivo Medium", 12, "Aceptar", QMessageBox.AcceptRole).exec()
                return
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

                    # Refrescar la tabla con los nuevos datos usando Polars
                    df = pl.read_database("SELECT id_cliente, nombre_cliente, telefono, email FROM cliente;", s.conn)
                    self.client_table.setRowCount(df.height)
                    for i, row in enumerate(df.iter_rows()):
                        for j, value in enumerate(row):
                            self.client_table.setItem(i, j, QTableWidgetItem(str(value)))
                except Exception as e:
                    print("Error al insertar el cliente:", e)
        def close():
            self.w.close()

        # Agregar QLineEdit para cada campo usando el texto como placeholder
        for i, (key, text) in enumerate(fields):
            row = i // 2 + 2  # 4 filas para campos, empezando en la fila 2
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
                case "tax_responsibility":
                    field_input.setMinimumWidth(275)
                case _:
                    pass

            setattr(self, f"{key}_input", field_input)
            self.w_layout.addWidget(getattr(self, f"{key}_input"), row, col, Qt.AlignLeft)

            # Conectar la tecla Enter para ejecutar command en cada campo
            field_input.returnPressed.connect(command)

        # Colocar los botones en la fila siguiente a los campos (fila 6)
        for i, (key, text) in enumerate(buttons):
            col = i % 2
            style = "accept" if key == "accept" else "cancel"
            setattr(self, f'btn_{key}', button.create_button(text, style, None, 16, (125, 50)))
            self.w_layout.addWidget(getattr(self, f'btn_{key}'), 6, col, Qt.AlignCenter)

        # Vincular la función command al botón "Aceptar"
        self.btn_accept.clicked.connect(command)
        self.btn_cancel.clicked.connect(close)

        self.w.show()

    def edit_client(self): #Método para editar los clientes 
        from service import s

        label = LabelFactory()
        button = ButtonFactory()
        msgbox = MsgBoxFactory()

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
        self.w.setWindowIcon(QIcon(resource_path("assets/pictures/AqualabLogo.jpg")))
        self.w.setStyleSheet("""background-color: white;""")
        self.w.setContentsMargins(20,20,20,20)
        self.w.setWindowFlags(Qt.WindowCloseButtonHint)
        
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
        selected_items = self.client_table.selectedItems()
        if not selected_items:
            q = msgbox.create_msg_box("information", "Información", "Selecciona un cliente a editar.", QMessageBox.Information, "Archivo Medium", 12, "Aceptar", QMessageBox.AcceptRole)
            q.exec()
            return
        row = selected_items[0].row()
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
            ("email", f"{self.client_table.item(row, 3).text()}"),
            ("fiscal_regime", details[6] if len(details) > 6 else ""),
            ("tax_responsibility", details[7] if len(details) > 7 else ""),
            ("economic_activity", details[8] if len(details) > 8 else "")
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
                ('email', self.email_input),
                ('fiscal_regime', self.fiscal_regime_input),
                ('tax_responsibility', self.tax_responsibility_input),
                ('economic_activity', self.economic_activity_input)
            ]
            values = [field.text() if field.text().strip() != '' else None for _, field in fields_values]
            # Solo los primeros 5 campos son obligatorios
            try:
                q = msgbox.create_question_box("question", "Información", "¿Deseas guardar los cambios?", QMessageBox.Question, "Archivo Medium", 12, ["Sí", "No"], [QMessageBox.AcceptRole, QMessageBox.RejectRole])
                q.exec()

                if q.clickedButton().text() == "Sí":
                    q2 = msgbox.create_msg_box("information", "Información", "Cliente editado correctamente", QMessageBox.Information, "Archivo Medium", 12, "Aceptar", QMessageBox.AcceptRole)
                    q2.exec()
                    s.edit_client(client_id, *values)
                    self.w.close()

                # Refrescar la tabla con los nuevos datos usando Polars
                df = pl.read_database("SELECT id_cliente, nombre_cliente, telefono, email FROM cliente;", s.conn)
                self.client_table.setRowCount(df.height)
                for i, row in enumerate(df.iter_rows()):
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
                case "tax_responsibility":
                    field_input.setMinimumWidth(275)
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
            self.w_layout.addWidget(getattr(self, f'btn_{key}'), 6, col, Qt.AlignCenter)

        # Vincular la función command al botón "Aceptar"
        self.btn_accept.clicked.connect(command)
        self.btn_cancel.clicked.connect(close)

        self.w.show()
    
    def delete_client(self): #Método para borrar un cliente
        from service import s
        
        msgbox = MsgBoxFactory()

        # Verificar que se haya seleccionado un cliente
        selected_items = self.client_table.selectedItems()
        if not selected_items:
            q = msgbox.create_msg_box("information", "Información", "Selecciona un cliente a eliminar.", QMessageBox.Information, "Archivo Medium", 12, "Aceptar", QMessageBox.AcceptRole)
            q.exec()
            return
        
        # Extraer el ID del cliente (asumiendo que está en la primera columna)
        row = selected_items[0].row()
        client_id_item = self.client_table.item(row, 0)
        client_id = client_id_item.text()
        
        try:
            q = msgbox.create_question_box("question", "Información", "¿Desea eliminar este cliente?", QMessageBox.Question, "Archivo Medium", 12, ["Sí", "No"], [QMessageBox.AcceptRole, QMessageBox.RejectRole])
            q.exec()

            if q.clickedButton().text() == "Sí":
                q2 = msgbox.create_msg_box("information", "Información", "Cliente eliminado correctamente", QMessageBox.Information, "Archivo Medium", 12, "Aceptar", QMessageBox.AcceptRole)
                q2.exec()
                s.delete_client(client_id)

                self.client_table.removeRow(row)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo eliminar el cliente: {e}")

    def show_details(self):
        from service import s
       
        # Obtener el ID del cliente
        selected_items = self.client_table.selectedItems()
        if not selected_items:
            return
        
        row = selected_items[0].row()
        
        client_id = self.client_table.item(row, 0).text()
        client_details = s.show_client_details(client_id)
        if not client_details:
            return

        details_text = ""
        labels = ["ID Cliente", "Nombre", "Cédula/NIT", "Dirección", "Teléfono", "Email", "Régimen Fiscal", "Responsabilidad Tributaria", "Actividad Económica"]
        for i, detail in enumerate(client_details[0]):
            details_text += f"<b>{labels[i]}:</b> {detail}<br>"
        
        msgbox = MsgBoxFactory()
        msg = msgbox.create_msg_box("information", "Detalles del Cliente", f"<h3>Detalles del Cliente</h3><p>{details_text}</p>",
                                    QMessageBox.NoIcon, "Archivo Medium", 12, "Volver", QMessageBox.AcceptRole)
        
        msg.exec()
    
    def export(self):
        Export().export_data("clients")

    def open_settings(self):
        from settings import SettingsWindow
        self.settings_window = SettingsWindow()
        self.settings_window.show()
