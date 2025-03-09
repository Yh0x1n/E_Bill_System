'''
Script de la ventana principal de la aplicación
'''
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QStatusBar, QHBoxLayout, QMainWindow, QMenuBar, QMenu, QPushButton, QWidgetAction, QMessageBox, QFrame, QStackedWidget, QSizePolicy
from PySide6.QtCore import QTimer, Qt, QPoint, QSize, QRect
from PySide6.QtGui import QIcon, QAction, QPixmap, QPainter, QBrush, QFontDatabase, QFont
import os, sys
from datetime import datetime


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        """font_paths = [
            os.path.abspath("src/fonts/Archivo-Regular.ttf"),
            os.path.abspath("src/fonts/Archivo-Bold.ttf"),
            os.path.abspath("src/fonts/Archivo-Medium.ttf"),
            os.path.abspath("src/fonts/Archivo-Black.ttf")
        ]
        for font_path in font_paths:
            id = QFontDatabase.addApplicationFont(font_path)
            if id < 0: print("Error")"""
    
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

        # Se crea el layout principal para colocar los widgets
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.sideBar)
        self.mainLayout.addWidget(self.dashboard)
        self.setLayout(self.mainLayout)
        
    def createSideBar(self): # Función para crear la barra lateral, ajustable según el tamaño de la ventana
        self.sideBar = QFrame(self)
        self.sideBar.setStyleSheet("background-color: blue;")
        self.sideBar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.sideBar.setMinimumWidth(300)
        self.sideBar.setMaximumWidth(350)
        self.sideBar.setFixedHeight(self.height())
        
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

        self.dashboardLayout = QVBoxLayout(self.dashboard)
        self.dashboardLayout.setContentsMargins(0, 0, 0, 0)
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
        self.menu_label = QLabel("Menú principal", self.dashboard)
        self.menu_label.setFont(QFont("Archivo Black", 32))
        self.menu_label.setStyleSheet("color: black;")
        self.menu_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.menu_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        #Etiqueta "Resumen", que va justo debajo de "Menú principal"
        self.res_label = QLabel("Resumen", self.dashboard)
        self.res_label.setFont(QFont("Archivo Black", 18))
        self.res_label.setStyleSheet("color: black;")
        self.res_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.res_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def createProfilePic(self):
        # Etiqueta para mostrar la foto de perfil del usuario
        self.profile_pic = QLabel(self.sideBar)
        self.profile_pic.setStyleSheet("background-color: white;"
                           "border-radius: 35px;")
        self.profile_pic.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.profile_pic.setGeometry(20, 20, 75, 75)
        self.setRoundedProfilePic("src/assets/AqualabLogo.jpg")
    
    def onResize(self, event): # Este evento ajusta el tamaño de los widgets, botones y etiquetas según la resolución de la ventana
        self.sideBar.setFixedHeight(self.height())
        self.dashboard.setFixedSize(self.width() - 300, self.height())
        
        # Ajustar la posición y el tamaño de los labels
        self.user_label.setGeometry(115, 40, self.sideBar.width(), 25)
        self.email_label.setGeometry(120, 65, self.sideBar.width(), 25)
        self.ver_label.setGeometry(20, self.sideBar.height() - 45, self.sideBar.width(), 20)
        self.date_label.move(self.sideBar.width() - self.date_label.width() - 20, self.sideBar.height() - self.date_label.height() - 70)
        self.menu_label.setGeometry(20, 35, self.dashboard.width(), 50)
        self.res_label.setGeometry(25, 90, self.dashboard.width(), 50)
        
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