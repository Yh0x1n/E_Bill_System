"""
Módulo de gestión de clientes
"""

from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QGridLayout, QPushButton, QListWidget
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
        
    def initUI(self):
        self.initHeader()
        self.initList()
        
    def initHeader(self):
        label = LabelFactory()
        button = ButtonFactory()

        self.headerLayout = QGridLayout()  # Cambiar a QGridLayout para organizar el header
        self.client_label = label.create_label("Clientes", "Archivo Black", "bold_black", 32)
        self.headerLayout.addWidget(self.client_label, 0, 0, 1, 3, Qt.AlignLeft)

        self.client_sublabel = label.create_label("Administra tus clientes", "Archivo Black", "bold_black", 16)
        self.headerLayout.addWidget(self.client_sublabel, 1, 0, 1, 3, Qt.AlignLeft)

        self.btn_settings = button.create_button("", "default_black", "src/assets/icons/settings.png", min_size = (75, 75))
        self.headerLayout.addWidget(self.btn_settings, 0, 3, 2, 2, Qt.AlignTop | Qt.AlignRight)

        self.clientLayout.addLayout(self.headerLayout)  # Añadir el headerLayout al layout principal

    def initList(self):
        self.client_list = QListWidget()
        self.client_list.setContentsMargins(5, 5, 5, 5)
        self.client_list.setSpacing(5)
        self.client_list.setStyleSheet("font-size: 14px;")
        self.client_list.setFont(QFont("Archivo Medium", 16))
        self.clientLayout.addWidget(self.client_list)
        self.load_clients()

    def load_clients(self):
        # Simular datos de clientes (puedes reemplazar esto con datos reales)
        clients = ["Cliente 1", "Cliente 2", "Cliente 3"]
        self.client_list.addItems(clients)