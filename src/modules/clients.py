"""
Módulo de gestión de clientes
"""

from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QGridLayout, QPushButton, QHBoxLayout, QTableWidget, QSizePolicy, QTableWidgetItem, QHeaderView, QDialog, QProgressBar
from PySide6.QtCore import Qt, QTimer
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
        self.initButtons()
        self.initList()
        
    def initHeader(self):
        label = LabelFactory()
        button = ButtonFactory()

        self.headerLayout = QGridLayout()  # Cambiar a QGridLayout para organizar el header
        self.client_label = label.create_label("Clientes", "Archivo Black", "bold_black", 32)
        self.headerLayout.addWidget(self.client_label, 0, 0, 1, 3, Qt.AlignLeft)

        self.client_sublabel = label.create_label("Administra tus clientes", "Archivo Black", "bold_black", 16)
        self.headerLayout.addWidget(self.client_sublabel, 1, 0, 1, 3, Qt.AlignLeft)

        self.clientLayout.addLayout(self.headerLayout)  # Añadir el headerLayout al layout principal

    def initButtons(self):
        button = ButtonFactory()

        self.buttonLayout = QGridLayout()
        self.buttonLayout.setContentsMargins(0, 100, 0, 0)
        self.buttonLayout.setSpacing(5)
        self.buttonLayout.setAlignment(Qt.AlignBottom)
        self.clientLayout.addLayout(self.buttonLayout)

        self.btn_settings = button.create_button("", "default_black", "src/assets/icons/settings.png", min_size = (75, 75))
        self.headerLayout.addWidget(self.btn_settings, 0, 3, 2, 2, Qt.AlignTop | Qt.AlignRight)
        
        self.btn_add = button.create_button("", "default_black", "src/assets/icons/Icon.png", min_size = (75, 75))
        self.buttonLayout.addWidget(self.btn_add, 4, 3, 3, 4, Qt.AlignBottom | Qt.AlignRight)

        self.btn_edit = button.create_button("", "default_black", "src/assets/icons/Pen.png", min_size = (75, 75))
        self.buttonLayout.addWidget(self.btn_edit, 4, 4, 3, 4, Qt.AlignBottom | Qt.AlignRight)

        self.btn_delete = button.create_button("", "default_black", "src/assets/icons/Trash.png", min_size = (75, 75))
        self.buttonLayout.addWidget(self.btn_delete, 4, 5, 3, 4, Qt.AlignBottom | Qt.AlignRight)

        description = ["Editar", "Agregar", "Eliminar", "Ajustes"]
        buttons = [self.btn_edit, self.btn_add, self.btn_delete, self.btn_settings]
        for i, button in enumerate(buttons):
            button.setToolTip(description[i])

    def initList(self):
        import pandas as pd
        from service import s

        self.listLayout = QVBoxLayout()
        self.listLayout.setAlignment(Qt.AlignBottom)
        self.listLayout.setContentsMargins(0, 0, 0, 0)
        self.clientLayout.addLayout(self.listLayout)

        # Fetch data from the database
        df = pd.read_sql("SELECT * FROM cliente;", s.conn)

        # Crear y configurar la tabla
        self.client_table = QTableWidget()
        self.client_table.setRowCount(len(df))
        self.client_table.setColumnCount(len(df.columns))
        self.client_table.setHorizontalHeaderLabels(["N°", "Nombre", "Cédula", "Dirección", "Teléfono", "Email"])
        self.client_table.setMinimumSize(600, 200)
        self.client_table.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.client_table.setStyleSheet("font-size: 14px;")
        self.client_table.setFont(QFont("Archivo Medium", 16))
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