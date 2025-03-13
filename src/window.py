'''
Script de la ventana principal de la aplicación
'''
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QStatusBar, QHBoxLayout, QMainWindow, QMenuBar, QMenu, QPushButton, QWidgetAction, QMessageBox, QFrame, QStackedWidget, QSizePolicy, QGridLayout
from PySide6.QtCore import QTimer, Qt, QPoint, QSize, QRect
from PySide6.QtGui import QIcon, QAction, QPixmap, QPainter, QBrush, QFontDatabase, QFont
import os, sys
from datetime import datetime


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
    
        self.setWindowIcon(QIcon("src/assets/AqualabLogo.jpg"))
        self.initUI()
        self.initDateTime()
        self.resize(1024, 600)
        self.setMinimumSize(1024, 600)
    
    def initUI(self):
        self.createSideBar()
        self.createDashboard()  # Asegúrate de crear el dashboard antes de añadirlo al layout
        self.createLabels()
        self.createProfilePic()
        self.createButtons()

        # Se crea el layout principal para colocar los widgets
        self.mainLayout = QGridLayout()
        self.mainLayout.addWidget(self.sideBar, 0, 0)
        self.mainLayout.addWidget(self.dashboard, 0, 1)
        self.setLayout(self.mainLayout)
        
    def createSideBar(self): # Función para crear la barra lateral, ajustable según el tamaño de la ventana
        self.sideBar = QFrame(self)
        self.sideBar.setStyleSheet("background-color: blue;")
        self.sideBar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.sideBar.setMinimumWidth(300)
        self.sideBar.setMaximumWidth(350)
        
        self.sideLayout = QVBoxLayout(self.sideBar)
        self.sideLayout.setContentsMargins(0, 0, 0, 0)
        self.sideLayout.setSpacing(0)
        
        self.sideBar.setLayout(self.sideLayout)
        
        self.resizeEvent = self.onResize

    def createDashboard(self): # Función para crear el dashboard donde irán ubicados los botones y etiquetas principales
        self.dashboard = QFrame(self)
        self.dashboard.setStyleSheet("background-color: white;")
        self.dashboard.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.dashboard.setGeometry(300, 0, self.width() - 300, self.height())

        self.dashboardLayout = QGridLayout(self.dashboard)
        self.dashboardLayout.setContentsMargins(20, 20, 20, 20)
        self.dashboardLayout.setSpacing(0)

        self.dashboard.setLayout(self.dashboardLayout)
        self.resizeEvent = self.onResize


    def createLabels(self): # Etiquetas responsivas y adaptables según el tamaño de la ventana

        # Etiqueta de usuario
        self.user_label = QLabel("Usuario", self.sideBar)
        self.user_label.setFont(QFont("Archivo Black", 20))
        self.user_label.setStyleSheet("color: white;")
        self.user_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.user_label.move(100, 50) #Posición inicial

        # Etiqueta de correo electrónico
        self.email_label = QLabel("Correo electrónico", self.sideBar)
        self.email_label.setFont(QFont("Archivo Medium", 10))
        self.email_label.setStyleSheet("color: gray;")
        self.email_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.email_label.move(120, 65) #Posición inicial

        # Etiqueta de la fecha
        self.date_label = QLabel("V1.0", self.sideBar)
        self.date_label.setFont(QFont("Archivo Medium", 14))
        self.date_label.setStyleSheet("color: white;")
        self.date_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.date_label.move(self.sideBar.width() - 100, self.sideBar.height() - 30)  # Posición inicial

        #Etiqueta de la versión del programa
        self.ver_label = QLabel("V1.0", self.sideBar)
        self.ver_label.setFont(QFont("Archivo Medium", 14))
        self.ver_label.setStyleSheet("color: white;")
        self.ver_label.setAlignment(Qt.AlignLeft | Qt.AlignBottom)
        self.ver_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Etiqueta "Menú principal"
        self.menu_label = QLabel("Menú principal")
        self.menu_label.setFont(QFont("Archivo Black", 32))
        self.menu_label.setStyleSheet("color: black;")
        self.menu_label.setContentsMargins(0, 0, 0, 0)
        self.menu_label.setAlignment(Qt.AlignLeft)
        self.dashboardLayout.setRowStretch(0, 0)
        self.dashboardLayout.addWidget(self.menu_label, 0, 0)

        # Etiqueta "Resumen", que va justo debajo de "Menú principal"
        self.res_label = QLabel("Resumen")
        self.res_label.setFont(QFont("Archivo Black", 18))
        self.res_label.setStyleSheet("color: black;")
        self.res_label.setAlignment(Qt.AlignTop)
        self.res_label.setContentsMargins(0, 0, 0, 0)
        self.dashboardLayout.addWidget(self.res_label, 1, 0)

        #Etiqueta "Total de ventas"
        self.total_label = QLabel("Total de ventas:")
        self.total_label.setFont(QFont("Archivo Black", 16))
        self.total_label.setStyleSheet("color: black;")
        self.dashboardLayout.addWidget(self.total_label, 1, 2)

        self.money = QLabel("$0.00")
        self.money.setFont(QFont("Archivo Medium", 16))
        self.money.setStyleSheet("color: blue;")
        self.dashboardLayout.addWidget(self.money, 2, 2)

    def createProfilePic(self):
        # Etiqueta para mostrar la foto de perfil del usuario
        self.profile_pic = QLabel(self.sideBar)
        self.profile_pic.setStyleSheet("background-color: white;"
                           "border-radius: 35px;")
        self.profile_pic.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.profile_pic.setGeometry(20, 20, 75, 75)
        self.setRoundedProfilePic("src/assets/AqualabLogo.jpg")
    
    def createButtons(self):
        # Crear un widget para contener el layout de botones
        self.buttonWidget = QWidget()
        self.buttonLayout = QGridLayout(self.buttonWidget)
        self.buttonLayout.setContentsMargins(0, 0, 0, 0)
        self.buttonLayout.setSpacing(10)
        self.buttonLayout.setAlignment(Qt.AlignBottom | Qt.AlignRight)
        self.dashboardLayout.addWidget(self.buttonWidget, 3, 0, 2, 3)  # Añadir el widget de botones en la fila 2, ocupando 2 columnas

        # Botones del dashboard
        # TO-DO: COLOCAR ÍCONOS A LOS BOTONES
        self.btn_facturas = QPushButton("Facturas")
        self.btn_facturas.setFont(QFont("Archivo Black", 16))
        self.btn_facturas.setStyleSheet("""background-color: #009345;
                                            color: white;
                                            border-radius: 10px;
                                            text-align: right bottom;
                                            padding: 15px;""")
        self.btn_facturas.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.btn_facturas.setMinimumSize(320, 120)
        self.buttonLayout.addWidget(self.btn_facturas, 0, 0)

        self.btn_clientes = QPushButton("Clientes")
        self.btn_clientes.setFont(QFont("Archivo Black", 16))
        self.btn_clientes.setStyleSheet("""background-color: #009345;
                                            color: white; 
                                            border-radius: 10px;
                                            text-align: right bottom;
                                            padding: 15px;""")
        self.btn_clientes.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.btn_clientes.setMinimumSize(225, 120)
        self.buttonLayout.addWidget(self.btn_clientes, 0, 1)

        self.btn_productos = QPushButton("Productos y servicios")
        self.btn_productos.setFont(QFont("Archivo Black", 16))
        self.btn_productos.setStyleSheet("""background-color: #009345;
                                            color: white; 
                                            border-radius: 10px;
                                            text-align: right bottom;
                                            padding: 15px;""")
        self.btn_productos.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.btn_productos.setMinimumSize(320, 120)
        self.buttonLayout.addWidget(self.btn_productos, 1, 0)

        self.btn_salir = QPushButton("Salir")
        self.btn_salir.setFont(QFont("Archivo Black", 16))
        self.btn_salir.setStyleSheet("""background-color: #E50202;
                                        color: white; 
                                        border-radius: 10px;
                                        text-align: right bottom;
                                        padding: 15px;""")
        self.btn_salir.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.btn_salir.setMinimumSize(225, 120)
        self.buttonLayout.addWidget(self.btn_salir, 1, 1)

    def onResize(self, event): # Este evento ajusta el tamaño de los widgets, botones y etiquetas según la resolución de la ventana
        self.sideBar.setFixedHeight(self.height())
        self.dashboard.setFixedSize(self.width() - 300, self.height())
        
        # Ajustar la posición y el tamaño de los labels
        self.user_label.setGeometry(115, 40, self.sideBar.width(), 25)
        self.email_label.setGeometry(120, 65, self.sideBar.width(), 25)
        self.ver_label.setGeometry(20, self.sideBar.height() - 45, self.sideBar.width(), 20)
        self.date_label.move(self.sideBar.width() - self.date_label.width() - 20, self.sideBar.height() - self.date_label.height() - 70)
        self.total_label.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        self.money.setAlignment(Qt.AlignRight)

        # Ajustar la posición y el tamaño de la foto de perfil
        self.profile_pic.setGeometry(20, 20, 75, 75)

        # Ajustar el tamaño de los botones
        self.btn_productos.setMaximumSize(700, 150)
        self.btn_facturas.setMaximumSize(700, 150)
        self.btn_clientes.setMaximumSize(self.dashboard.width() // 3 - 10, 150)
        self.btn_salir.setMaximumSize(self.dashboard.width() // 3 - 10, 150)


        event.accept()

    def setRoundedProfilePic(self, image_path):
        pixmap = QPixmap(image_path).scaled(75, 75, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        mask = QPixmap(pixmap.size())
        mask.fill(Qt.transparent)

        painter = QPainter(mask)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(Qt.black))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(pixmap.rect(), 37.5, 37.5)
        painter.end()

        rounded = pixmap.copy()
        rounded.setMask(mask.createMaskFromColor(Qt.transparent, Qt.MaskInColor))

        self.profile_pic.setPixmap(rounded)

    def initDateTime(self): # Función para mostrar la fecha actual
        now = datetime.now()
        self.date_label.setText(now.strftime("%d/%m/%Y"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())