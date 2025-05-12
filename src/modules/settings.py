"""
Módulo con un widget de ventana para configurar el tema, gestionar los usuarios y la información del proveedor
"""

#Importaciones
from PySide6.QtWidgets import QWidget, QPushButton, QGridLayout, QLabel, QLineEdit, QComboBox, QTableWidget, QSizePolicy, QTableWidgetItem, QHeaderView, QMainWindow, QMessageBox
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
from window import MainWindow
import pandas as pd
from styles.buttons import ButtonFactory
from styles.labels import LabelFactory
from styles.msg_boxes import MsgBoxFactory
from service import s
import qdarktheme
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
        self.setWindowTitle("Configuración")
        self.setGeometry(100, 100, 300, 200)

        self.settings_layout = QGridLayout()
        self.setLayout(self.settings_layout)
        self.initUI()
        self.init_user_list()

    def initUI(self):

        # Combobox para colocar el tema
        self.theme_box = QComboBox()
        self.theme_box.setPlaceholderText("Tema de la aplicación")
        self.theme_box.addItems(["Tema Claro", "Tema Oscuro"])
        self.settings_layout.addWidget(self.theme_box, 0, 0, 1, 2)  # Fila 0, columna 0-1

        # Botón para aplicar cambios de tema
        self.apply_theme_button = QPushButton("Aplicar Tema")
        self.apply_theme_button.clicked.connect(self.apply_theme)
        self.settings_layout.addWidget(self.apply_theme_button, 0, 2)  # Fila 0, columna 2

        # Gestión de usuarios
        self.user_label = QLabel("Gestión de Usuarios:")
        self.settings_layout.addWidget(self.user_label, 1, 0, 1, 3)  # Fila 1, columna 0-2

        # Botón para editar el  usuario
        self.edit_user_button = QPushButton("Editar Usuario")
        self.edit_user_button.clicked.connect(self.edit_user)
        self.settings_layout.addWidget(self.edit_user_button, 2, 0)  # Fila 2, columna 0

        #Botón para eliminar el usuario
        self.edit_user_button = QPushButton("Eliminar Usuario")
        self.edit_user_button.clicked.connect(self.delete_user)
        self.settings_layout.addWidget(self.edit_user_button, 2, 1)  # Fila 2, columna 2

        # Información del proveedor
        self.provider_info_label = QLabel("Información del Proveedor:")
        self.settings_layout.addWidget(self.provider_info_label, 3, 0, 1, 3)  # Fila 3, columna 0-2

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
            from service import s
            import pandas as pd

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

    def delete_user(self):
        pass

    def apply_theme(self):  # Método para aplicar hojas de estilo de tema claro y oscuro
        pass