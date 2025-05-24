"""
Módulo con un widget de ventana para configurar el tema, gestionar los usuarios y la información del proveedor
"""

#TO-DO: ARREGLAR LOS ESTILOS Y ALINEACIÓN DE LOS BOTONES

#Importaciones
from PySide6.QtWidgets import QWidget, QPushButton, QGridLayout, QLabel, QLineEdit, QComboBox, QTableWidget, QSizePolicy, QTableWidgetItem, QHeaderView, QMainWindow, QMessageBox
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
import pandas as pd
from styles.buttons import ButtonFactory
from styles.labels import LabelFactory
from styles.msg_boxes import MsgBoxFactory
from service import s
from styles.lists import apply_table_style

class SettingsWindow(QWidget):
    """
    Clase que representa la ventana de configuración de la aplicación.
    Permite al usuario cambiar el tema, gestionar usuarios y ver información del proveedor.
    """
    def __init__(self):
        """
        Constructor de la ventana de configuración.
        :param main_window_instance: Instancia de la ventana principal (MainWindow).
        """
        super().__init__()
        self.setWindowTitle("Ajustes")
        self.setGeometry(100, 100, 300, 200)

        self.settings_layout = QGridLayout()
        self.setLayout(self.settings_layout)
        self.initUI()
        self.init_user_list()

    def initUI(self):
        label = LabelFactory()
        button = ButtonFactory()

        # Label de información del proveedor
        self.provider_label = label.create_label("Información del proveedor", "Archivo Medium", "medium_black", 14)
        self.settings_layout.addWidget(self.provider_label, 0, 0)

        # Botón para mostrar información del proveedor
        self.show_provider_info_button = button.create_button("Mostrar", "default_black", None, 12, (100, 40))
        self.show_provider_info_button.clicked.connect(self.show_provider_info)
        self.settings_layout.addWidget(self.show_provider_info_button, 0, 1)

        # Botón para editar la información del proveedor
        self.edit_provider_info_button = button.create_button("Editar", "default_black", None, 12, (100, 40))
        self.edit_provider_info_button.clicked.connect(self.set_provider_info)
        self.settings_layout.addWidget(self.edit_provider_info_button, 0, 2)

        # Gestión de usuarios
        self.user_label = label.create_label("Gestión de Usuarios:", "Archivo Medium", "medium_black", 14)
        self.settings_layout.addWidget(self.user_label, 1, 0, 1, 3)

        # Botón para editar el usuario
        self.edit_user_button = button.create_button("Editar Usuario", "accept", None, 12, (120, 40))
        self.edit_user_button.clicked.connect(self.edit_user)
        self.settings_layout.addWidget(self.edit_user_button, 2, 0)

        # Botón para eliminar el usuario
        self.delete_user_button = button.create_button("Eliminar Usuario", "cancel", None, 12, (120, 40))
        self.delete_user_button.clicked.connect(self.delete_user)
        self.settings_layout.addWidget(self.delete_user_button, 2, 1)

        # Información de usuarios
        self.provider_info_label = label.create_label("Información de usuarios:", "Archivo Medium", "medium_black", 14)
        self.settings_layout.addWidget(self.provider_info_label, 3, 0, 1, 3)

    def init_user_list(self):
        # Método que inicializa la lista de los usuarios registrados en la DB
        df = pd.read_sql_query("SELECT id, username, email FROM usuario;", s.conn)

        self.user_table = QTableWidget()
        self.user_table.setRowCount(len(df))
        self.user_table.setColumnCount(len(df.columns))
        self.user_table.setHorizontalHeaderLabels(["ID", "Nombre", "Email"])
        self.user_table.setMinimumSize(600, 200)
        self.user_table.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.user_table.setFont(QFont("Archivo Medium", 12))
        self.user_table.setEditTriggers(QTableWidget.NoEditTriggers)

        # Llenar la tabla con datos
        for i, row in df.iterrows():
            for j, value in enumerate(row):
                self.user_table.setItem(i, j, QTableWidgetItem(str(value)))

        self.settings_layout.addWidget(self.user_table, 4, 0, 1, 3)  # Fila 4, columna 0-2

        button = ButtonFactory()
        self.btn_salir = button.create_button("Salir", "exit", None, 10, (75, 35))
        self.btn_salir.clicked.connect(self.close)
        self.settings_layout.addWidget(self.btn_salir, 5, 2, 1, 3)

        # Ajustar el tamaño de las columnas según la longitud de sus campos
        self.user_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.user_table.horizontalHeader().setStretchLastSection(True)

        # Apply styles to the user table
        apply_table_style(self.user_table)

    def edit_user(self):
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
        self.w.setWindowTitle("Lanchmann - Editar Usuario")
        self.w.setStyleSheet("""background-color: white;""")
        self.w.setContentsMargins(10, 10, 10, 10)
        self.w.setWindowFlags(Qt.WindowCloseButtonHint)

        central_widget = QWidget(self.w)
        central_widget.setContentsMargins(10, 10, 10, 10)
        central_widget.setStyleSheet("background-color: #f0f0f0; border-radius: 20px;")
        self.w.setCentralWidget(central_widget)

        self.w_layout = QGridLayout()
        self.w_layout.setContentsMargins(5, 5, 5, 5)
        self.w_layout.setSpacing(10)
        central_widget.setLayout(self.w_layout)

        # Header label for the "Editar Usuario" section
        header_label = label.create_label("Editar Usuario", "Archivo Medium", "medium_black", 20)
        header_sublabel = label.create_label("Especifica los campos que desees editar", "Archivo Medium", "medium_black", 12)
        self.w_layout.addWidget(header_label, 0, 0, Qt.AlignLeft)
        self.w_layout.addWidget(header_sublabel, 1, 0, 1, 4, Qt.AlignLeft | Qt.AlignTop)

        # Campos de texto y botones
        selected_items = self.user_table.selectedItems()
        if not selected_items:
            q = msgbox.create_msg_box("information", "Información", "Selecciona un usuario a editar.", QMessageBox.Information, "Archivo Medium", 12, "Aceptar", QMessageBox.AcceptRole)
            q.exec()
            return
        row = selected_items[0].row()
        user_id = self.user_table.item(row, 0).text()

        user_details = s.show_user_details((user_id,))
        if user_details:
            details = user_details[0]  # Assumes the result is a tuple: (id, username, email)
            email = details[2]
        else:
            email = ""

        fields = [
            ("username", f"{self.user_table.item(row, 1).text()}"),
            ("email", email)
        ]

        buttons = [("accept", "Aceptar"), ("cancel", "Cancelar")]

        def command():

            # Obtener los valores de cada campo
            fields_values = [
                ('username', self.username_input),
                ('email', self.email_input)
            ]

            values = [field.text() for _, field in fields_values]

            try:
                q = msgbox.create_question_box("question", "Información", "¿Deseas guardar los cambios?", QMessageBox.Question, "Archivo Medium", 12, ["Sí", "No"], [QMessageBox.AcceptRole, QMessageBox.RejectRole])
                q.exec()

                if q.clickedButton().text() == "Sí":
                    q2 = msgbox.create_msg_box("information", "Información", "Usuario editado correctamente", QMessageBox.Information, "Archivo Medium", 12, "Aceptar", QMessageBox.AcceptRole)
                    q2.exec()
                    s.edit_user(user_id, *values)
                    self.w.close()

                # Refrescar la tabla con los nuevos datos
                df = pd.read_sql("SELECT id, username, email FROM usuario;", s.conn)
                self.user_table.setRowCount(len(df))
                for i, row in df.iterrows():
                    for j, value in enumerate(row):
                        self.user_table.setItem(i, j, QTableWidgetItem(str(value)))

            except Exception as e:
                print("Error al editar el usuario:", e)

        def close():
            self.w.close()

        for i, (key, text) in enumerate(fields):
            row = ((i // 2) * 2) + 2  # Empezar en la fila 1, luego filas 1-2, 3-4, etc.
            col = i % 2

            field_input = QLineEdit()
            field_input.setStyleSheet(input_stylesheet)
            field_input.setPlaceholderText(str(text))

            setattr(self, f"{key}_input", field_input)
            self.w_layout.addWidget(getattr(self, f"{key}_input"), row, col, Qt.AlignLeft)

            # Conectar la tecla Enter para ejecutar command en cada campo
            field_input.returnPressed.connect(command)

        for i, (key, text) in enumerate(buttons):
            col = i % 2
            style = "accept" if key == "accept" else "cancel"
            setattr(self, f'btn_{key}', button.create_button(text, style, None, 16, (100, 50)))
            self.w_layout.addWidget(getattr(self, f'btn_{key}'), 7, col, Qt.AlignCenter)

        # Vincular la función command al botón "Aceptar"
        self.btn_accept.clicked.connect(command)
        self.btn_cancel.clicked.connect(close)

        self.w.show()

    #TO-DO: CREAR LA LÓGICA DE ESTOS MÓDULOS
    def delete_user(self):
        pass

    def set_provider_info(self):
        """
        Método para establecer la información del proveedor.
        """

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

        self.provider_window = QMainWindow()
        self.provider_window.setWindowTitle("Editar Información del Proveedor")
        self.provider_window.setStyleSheet("background-color: white;")
        self.provider_window.setWindowFlags(Qt.WindowCloseButtonHint)

        central_widget = QWidget(self.provider_window)
        central_widget.setStyleSheet("background-color: #f0f0f0; border-radius: 20px;")
        self.provider_window.setCentralWidget(central_widget)

        layout = QGridLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        central_widget.setLayout(layout)

        # Obtener datos actuales del proveedor (si existen)
        s.cur.execute("SELECT nombre, nit, direccion, telefono, email FROM proveedor LIMIT 1;")
        proveedor = s.cur.fetchone()
        proveedor = proveedor if proveedor else ("", "", "", "", "")

        fields = [
            ("nombre", "Nombre", proveedor[0]),
            ("nit", "NIT", proveedor[1]),
            ("direccion", "Dirección", proveedor[2]),
            ("telefono", "Teléfono", proveedor[3]),
            ("email", "Email", proveedor[4])
        ]

        self.provider_inputs = {}
        for i, (key, label_text, value) in enumerate(fields):
            lbl = label.create_label(label_text, "Archivo Medium", "medium_black", 14)
            inp = QLineEdit()
            inp.setStyleSheet(input_stylesheet)
            inp.setPlaceholderText(label_text)
            inp.setText(str(value))
            self.provider_inputs[key] = inp
            layout.addWidget(lbl, i, 0)
            layout.addWidget(inp, i, 1)

        # Botones
        btn_save = button.create_button("Guardar", "accept", None, 16, (100, 40))
        btn_cancel = button.create_button("Cancelar", "cancel", None, 16, (100, 40))
        layout.addWidget(btn_save, len(fields), 0)
        layout.addWidget(btn_cancel, len(fields), 1)

        def save_provider():
            data = {k: self.provider_inputs[k].text().strip() for k in self.provider_inputs}
            if not all(data.values()):
                q = msgbox.create_msg_box("warning", "Advertencia", "Todos los campos son obligatorios.", QMessageBox.Warning, "Archivo Medium", 12, "Aceptar", QMessageBox.AcceptRole)
                q.exec()
                return

            try:
                # Si ya existe un proveedor, actualiza; si no, inserta
                s.cur.execute("SELECT COUNT(*) FROM proveedor;")
                exists = s.cur.fetchone()[0] > 0
                if exists:
                    s.cur.execute("""
                    UPDATE proveedor SET nombre=?, nit=?, direccion=?, telefono=?, email=?
                    """, (data["nombre"], data["nit"], data["direccion"], data["telefono"], data["email"]))
                else:
                    s.cur.execute("""
                    INSERT INTO proveedor(nombre, nit, direccion, telefono, email)
                    VALUES (?, ?, ?, ?, ?)
                    """, (data["nombre"], data["nit"], data["direccion"], data["telefono"], data["email"]))
                s.conn.commit()
                q = msgbox.create_msg_box("information", "Éxito", "Información del proveedor guardada correctamente.", QMessageBox.Information, "Archivo Medium", 12, "Aceptar", QMessageBox.AcceptRole)
                q.exec()
                self.provider_window.close()
            except Exception as e:
                print("Error al guardar la información del proveedor:", e)
                q = msgbox.create_msg_box("critical", "Error", "No se pudo guardar la información.", QMessageBox.Critical, "Archivo Medium", 12, "Aceptar", QMessageBox.AcceptRole)
                q.exec()

        btn_save.clicked.connect(save_provider)
        btn_cancel.clicked.connect(self.provider_window.close)
        self.provider_window.show()
    
    def show_provider_info(self):
        label = LabelFactory()
        msgbox = MsgBoxFactory()

        # Obtener datos actuales del proveedor (si existen)
        s.cur.execute("SELECT nombre, nit, direccion, telefono, email FROM proveedor LIMIT 1;")
        proveedor = s.cur.fetchone()

        if not proveedor:
            q = msgbox.create_msg_box(
                "information",
                "Información",
                "No hay información del proveedor registrada.",
                QMessageBox.Information,
                "Archivo Medium",
                12,
                "Aceptar",
                QMessageBox.AcceptRole
            )
            q.exec()
            return

        # Usar LabelFactory para el título y los campos
        info_labels = [
            label.create_label(f"Nombre: {proveedor[0]}", "Archivo Medium", "medium_black", 12),
            label.create_label(f"NIT: {proveedor[1]}", "Archivo Medium", "medium_black", 12),
            label.create_label(f"Dirección: {proveedor[2]}", "Archivo Medium", "medium_black", 12),
            label.create_label(f"Teléfono: {proveedor[3]}", "Archivo Medium", "medium_black", 12),
            label.create_label(f"Email: {proveedor[4]}", "Archivo Medium", "medium_black", 12)
        ]
        info_text = "<br>".join([lbl.text() for lbl in info_labels])

        q = msgbox.create_msg_box(
            "information",
            "Información del Proveedor",
            info_text,
            QMessageBox.Information,
            "Archivo Medium",
            12,
            "Aceptar",
            QMessageBox.AcceptRole
        )
        q.exec()