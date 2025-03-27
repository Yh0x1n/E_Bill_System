'''
Script de la ventana principal de la aplicación
'''
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QMainWindow, QMessageBox, QFrame, QSizePolicy, QGridLayout, QLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QPixmap, QPainter, QBrush, QFont
import os, sys
from datetime import datetime
from styles.buttons import ButtonFactory
from styles.labels import LabelFactory
from styles.msg_boxes import MsgBoxFactory
class MainWindow(QMainWindow):
    def __init__(self, username, email):
        super().__init__()
    
        self.setWindowIcon(QIcon("src/assets/AqualabLogo.jpg"))
        self.resize(1024, 600)
        self.setMinimumSize(1024, 600)
        [method() for method in (self.initUI, self.initDateTime, lambda: self.initUser(username, email))]

    def initUI(self):
        [method() for method in (self.createSideBar, self.createDashboard, self.createProfilePic, self.createLabels, self.createButtons)]

        # Se crea el layout principal para colocar los widgets
        self.mainLayout = QGridLayout()
        self.mainLayout.addWidget(self.sideBar, 0, 0)
        self.mainLayout.addWidget(self.dashboard, 0, 1)
        self.setLayout(self.mainLayout)
        
    def createSideBar(self): # Función para crear la barra lateral, ajustable según el tamaño de la ventana
        self.sideBar = QFrame(self)
        self.sideBar.setStyleSheet("background-color: blue;")
        self.sideBar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.sideBar.setMinimumWidth(350)
        self.sideBar.setMaximumWidth(350)
        
        self.sideLayout = QVBoxLayout(self.sideBar)
        self.sideLayout.setContentsMargins(20, 20, 20, 20)
        self.sideLayout.setSpacing(0)
        self.sideBar.setLayout(self.sideLayout)

        self.sideTopLayout = QGridLayout()
        self.sideTopLayout.setAlignment(Qt.AlignTop)
        self.sideLayout.addLayout(self.sideTopLayout)

        self.sideMidTopLayout = QVBoxLayout()
        self.sideLayout.addLayout(self.sideMidTopLayout)

        self.sideMidLowLayout = QHBoxLayout()
        self.sideLayout.addLayout(self.sideMidLowLayout)
        
        self.sideBottomLayout = QHBoxLayout()
        self.sideBottomLayout.setAlignment(Qt.AlignBottom)
        self.sideLayout.addLayout(self.sideBottomLayout)
        
        self.resizeEvent = self.onResize

    def createDashboard(self): # Función para crear el dashboard donde irán ubicados los botones y etiquetas principales
        self.dashboard = QFrame(self)
        self.dashboard.setStyleSheet("background-color: white;")
        self.dashboard.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.dashboard.setGeometry(350, 0, self.width() - 350, self.height())

        self.dashboardLayout = QVBoxLayout(self.dashboard)
        self.dashboardLayout.setContentsMargins(20, 20, 20, 20)
        self.dashboardLayout.setSpacing(0)
        self.dashboard.setLayout(self.dashboardLayout)

        self.dashboardHeader = QGridLayout()
        self.dashboardHeader.setAlignment(Qt.AlignTop)
        self.dashboardLayout.addLayout(self.dashboardHeader)
        
        self.dashboardMidLayout = QVBoxLayout()
        self.dashboardMidLayout.setAlignment(Qt.AlignRight | Qt.AlignLeft)
        self.dashboardLayout.addLayout(self.dashboardMidLayout)

        self.dashboardBottomLayout = QVBoxLayout()
        self.dashboardBottomLayout.setAlignment(Qt.AlignBottom)
        self.dashboardLayout.addLayout(self.dashboardBottomLayout)

        self.resizeEvent = self.onResize
    
    def createProfilePic(self):
        # Etiqueta para mostrar la foto de perfil del usuario
        self.profile_pic = QLabel(self.sideBar)
        self.profile_pic.setStyleSheet("background-color: white;"
                        "border-radius: 35px;")
        self.profile_pic.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.profile_pic.setFixedSize(75, 75)
        self.sideTopLayout.addWidget(self.profile_pic, 0, 0, 3, 3, Qt.AlignLeft | Qt.AlignBottom)
        self.setRoundedProfilePic("src/assets/pictures/AqualabLogo.jpg")


    def createLabels(self): # Etiquetas responsivas y adaptables según el tamaño de la ventana
        # Etiqueta de usuario
        label = LabelFactory()

        # Etiqueta de usuario
        self.user_label = label.create_label("Usuario", font="Archivo Black", style="bold_white", font_size=20)
        self.user_label.setStyleSheet(self.user_label.styleSheet())
        self.sideTopLayout.addWidget(self.user_label, 0, 1, 3, 5, Qt.AlignCenter)

        # Etiqueta de correo electrónico
        self.email_label = label.create_label("Correo electrónico", font= "Archivo Medium", style="medium_white", font_size=10)
        self.sideTopLayout.addWidget(self.email_label, 2, 1, 3, 5, Qt.AlignCenter)

        # Etiqueta de la fecha
        self.date_label = label.create_label("", font="Archivo Medium", style="medium_white", font_size=14)
        self.sideMidLowLayout.addWidget(self.date_label, 0, Qt.AlignBottom | Qt.AlignRight)

        # Etiqueta de la versión del programa
        self.ver_label = label.create_label("V1.0", font="Archivo Medium", style="medium_white", font_size=14)
        self.ver_label.setStyleSheet(self.ver_label.styleSheet())
        self.sideBottomLayout.addWidget(self.ver_label, 0, Qt.AlignBottom | Qt.AlignLeft)

        # Etiqueta "Menú principal"
        self.menu_label = label.create_label("Menú principal",font="Archivo Black", style="bold_black", font_size=32)
        self.menu_label.setAlignment(Qt.AlignLeft)
        self.dashboardHeader.addWidget(self.menu_label, 0, 0, 1, 5)

        # Etiqueta "Resumen", que va justo debajo de "Menú principal"
        self.res_label = label.create_label("Resumen",font="Archivo Black", style="bold_black", font_size=18)
        self.res_label.setAlignment(Qt.AlignTop)
        self.dashboardHeader.addWidget(self.res_label, 1, 0, 1, 3)

        # Etiqueta "Total de ventas"
        self.total_label = label.create_label("Total de ventas", font="Archivo Medium", style="medium_black", font_size=16)
        self.dashboardMidLayout.addWidget(self.total_label, Qt.AlignRight | Qt.AlignBottom)

        self.money = label.create_label("$0.00", font="Archivo Medium", style="money", font_size=24)
        self.dashboardMidLayout.addWidget(self.money, Qt.AlignRight | Qt.AlignBottom)
    
    def createButtons(self):
        button = ButtonFactory()

        # Widget para contener el layout de botones
        self.buttonWidget = QWidget()
        self.buttonLayout = QGridLayout(self.buttonWidget)
        self.buttonLayout.setContentsMargins(0, 0, 0, 0)
        self.buttonLayout.setSpacing(10)
        self.buttonLayout.setAlignment(Qt.AlignBottom | Qt.AlignRight)
        self.dashboardBottomLayout.addWidget(self.buttonWidget)  # Añadir el widget de botones en la fila 2, ocupando 2 columnas

        # BOTONES DE LA SIDEBAR
        self.btn_logout = button.create_button("Cerrar sesión", style="logout", font_size=14, min_size=(0, 0))
        self.sideBottomLayout.addWidget(self.btn_logout, 0, Qt.AlignBottom | Qt.AlignRight)
        self.btn_logout.clicked.connect(self.logout)

        self.btn_ventas = button.create_button("Tus últimas ventas", style="sales", font_size=14, min_size=(200, 0))
        self.sideMidTopLayout.addWidget(self.btn_ventas, 0, Qt.AlignLeft)
        self.btn_ventas.clicked.connect(self.display_ventas)

        self.btn_gestionar_facturas = button.create_button("Gestionar facturas", style = "sales", font_size=14, min_size=(200,0))
        self.sideMidTopLayout.addWidget(self.btn_gestionar_facturas, 0, Qt.AlignLeft)
        
        self.btn_ayuda = button.create_button("Ayuda", style = "sales", font_size=14, min_size=(100,0))
        self.sideMidTopLayout.addWidget(self.btn_ayuda, 0, Qt.AlignLeft)

        self.btn_about = button.create_button("Acerca de", style = "sales", font_size=14, min_size=(130,0))
        self.sideMidTopLayout.addWidget(self.btn_about, 0, Qt.AlignLeft)

        # BOTONES DEL DASHBOARD
        self.btn_facturas = button.create_button("Facturas", icon_path="src/assets/icons/Clipboard.png")
        self.buttonLayout.addWidget(self.btn_facturas, 0, 0)

        self.btn_clientes = button.create_button("Clientes", icon_path="src/assets/icons/Briefcase.png")
        self.buttonLayout.addWidget(self.btn_clientes, 0, 1)

        self.btn_productos = button.create_button("Productos y servicios", icon_path="src/assets/icons/dollarSign.png")
        self.buttonLayout.addWidget(self.btn_productos, 1, 0)

        self.btn_salir = button.create_button("Salir", style="exit", icon_path="src/assets/icons/Xsquare.png")
        self.buttonLayout.addWidget(self.btn_salir, 1, 1)
        self.btn_salir.clicked.connect(self.close_window)

    def onResize(self, event): # Este evento ajusta el tamaño de los widgets, botones y etiquetas según la resolución de la ventana
        self.sideBar.setFixedHeight(self.height())
        self.dashboard.setFixedSize(self.width() - 350, self.height())
        
        # Ajustar la posición y el tamaño de los labels
        self.total_label.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        self.money.setAlignment(Qt.AlignRight)

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
    
    def logout(self):
        from login import LoginWindow

        q = MsgBoxFactory()
        response = q.create_question_box("question", "Información", "¿Quieres cerrar sesión?", QMessageBox.Information, "Archivo Medium", 12, ["Sí", "No"], [QMessageBox.AcceptRole, QMessageBox.RejectRole])
        response.exec()
        if response.clickedButton().text() == "Sí":  # Verifica si el botón "Sí" fue presionado
            self.close()
            self.login_window = LoginWindow()
            self.login_window.show()

    def display_ventas(self):
        # Método que alterna entre mostrar y ocultar las últimas facturas
        if hasattr(self, 'ventasWidget') and self.ventasWidget.isVisible():
            # Si las facturas están visibles, ocultarlas y mostrar los botones originales
            self.ventasWidget.setVisible(False)
            self.sideMidTopLayout.removeWidget(self.ventasWidget)
            for i in range(self.sideMidTopLayout.count()):
                widget = self.sideMidTopLayout.itemAt(i).widget()
                if widget and widget != self.btn_ventas:
                    widget.show()
        else:
            # Si las facturas no están visibles, ocultar los botones originales excepto el botón de ventas
            for i in range(self.sideMidTopLayout.count()):
                widget = self.sideMidTopLayout.itemAt(i).widget()
                if widget and widget != self.btn_ventas:
                    widget.hide()

            if not hasattr(self, 'ventasWidget'):
                # Crear un nuevo widget para mostrar las facturas si no existe
                self.ventasWidget = QWidget()
                self.ventasLayout = QVBoxLayout(self.ventasWidget)
                self.ventasLayout.setContentsMargins(0, 0, 0, 0)
                self.ventasLayout.setSpacing(5)
                self.sideMidTopLayout.addWidget(self.ventasWidget)

                from modules.service import s  # Importar el módulo de base de datos
                facturas = s.get_last_facturas()[:5]  # Obtener las últimas 5 facturas

                # Mostrar las facturas en etiquetas
                for factura in facturas:
                    factura_label = QLabel(f"Factura #{factura['id']}: {factura['cliente']} - ${factura['total']}")
                    factura_label.setStyleSheet("font-size: 14px; color: black;")
                    self.ventasLayout.addWidget(factura_label)
            self.sideMidTopLayout.addWidget(self.ventasWidget)
            self.ventasWidget.setVisible(True)
            self.ventasWidget.setVisible(True)
    def initDateTime(self): # Función para mostrar la fecha actual
        now = datetime.now()
        self.date_label.setText(now.strftime("%d/%m/%Y"))
    
    def initUser(self, username, email):
        # Mostrar el usuario que inició sesión
        self.user_label.setText(username)
        self.email_label.setText(email)
    
    def close_window(self):
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())