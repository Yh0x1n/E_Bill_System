"""
Módulo con un widget de ventana para configurar el tema, gestionar los usuarios y la información del proveedor
"""

#Importaciones
from PySide6.QtWidgets import QWidget, QPushButton, QGridLayout, QLabel, QLineEdit, QComboBox, QTableWidget, QSizePolicy, QTableWidgetItem, QHeaderView
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
from window import MainWindow
import pandas as pd
from service import s
import qdarktheme

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
        self.settings_layout.addWidget(self.edit_user_button, 2, 0)  # Fila 2, columna 2

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
    
    def edit_user(self):
        pass

    def delete_user(self):
        pass

    def apply_theme(self):  # Método para aplicar hojas de estilo de tema claro y oscuro
        pass