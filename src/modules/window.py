'''
Módulo de la ventana principal de la aplicación
'''
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QMainWindow, QMessageBox, QFrame, QSizePolicy, QGridLayout, QLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QPixmap, QPainter, QBrush, QFont, QColor
from PySide6.QtCharts import QChart, QChartView, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
from PySide6.QtCharts import QPieSeries, QPieSlice
from service import s
from datetime import datetime
from styles.buttons import ButtonFactory
from styles.labels import LabelFactory
from styles.msg_boxes import MsgBoxFactory
import os, sys

class MainWindow(QMainWindow):
    def __init__(self, username, email):
        super().__init__()
        self.setWindowTitle("Lachmann Invoice Generator")
        self.setWindowIcon(QIcon("src/assets/pictures/AqualabLogo.jpg"))
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

        self.sideMidTopLayout = QGridLayout()
        self.sideLayout.addLayout(self.sideMidTopLayout)

        self.sideMidLowLayout = QHBoxLayout()
        self.sideLayout.addLayout(self.sideMidLowLayout)
        
        self.sideBottomLayout = QHBoxLayout()
        self.sideBottomLayout.setAlignment(Qt.AlignBottom)
        self.sideLayout.addLayout(self.sideBottomLayout)
        
        self.resizeEvent = self.onResize

    def createDashboard(self): # Función para crear el dashboard donde irán ubicados los botones y etiquetas principales
        self.dashboard = QFrame(self)
        self.dashboard.setObjectName("dashboard")
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
        
        self.dashboardMidLayout = QGridLayout()
        self.dashboardLayout.addLayout(self.dashboardMidLayout)

        self.dashboardBottomLayout = QGridLayout()
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
        self.dashboardMidLayout.addWidget(self.total_label, 1, 1, Qt.AlignRight)

        self.money = label.create_label(str(f"${s.get_total_amount_invoices()}"), font="Archivo Medium", style="money", font_size=24)
        self.dashboardMidLayout.addWidget(self.money, 2, 1, Qt.AlignRight | Qt.AlignBottom)

        # Gráfico de resumen de clientes, productos y facturas
        def get_dashboard_counts():
            return (
            s.cur.execute("SELECT COUNT(*) FROM cliente").fetchone()[0],
            s.cur.execute("SELECT COUNT(*) FROM producto").fetchone()[0],
            s.cur.execute("SELECT COUNT(*) FROM facturas").fetchone()[0]
            )

        def set_pie_series(series, counts):
            labels = ["Clientes registrados", "Productos registrados", "Facturas generadas"]
            colors = [QColor("#009345"), QColor("#E50202"), QColor("#3302E5")]
            series.clear()
            for i, (label, count) in enumerate(zip(labels, counts)):
                slice = series.append(label, count)
                max_value = max(counts)
            
            for i, slice in enumerate(series.slices()):
                slice.setBrush(colors[i % len(colors)])
            
            if slice.value() == max_value and max_value > 0:
                slice.setExploded(True)
                slice.setLabelVisible(False)
                slice.setPen(QColor(Qt.black))
            else:
                slice.setLabelVisible(False)

        clientes_count, productos_count, facturas_count = get_dashboard_counts()
        
        self.series = QPieSeries()
        set_pie_series(self.series, (clientes_count, productos_count, facturas_count))

        self.chart = QChart()
        self.chart.addSeries(self.series)
        self.chart.legend().setAlignment(Qt.AlignRight)

        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)
        self.chart_view.setFixedSize(475, 175)
        self.dashboardMidLayout.addWidget(self.chart_view, 0, 0, Qt.AlignLeft)

        def update_dashboard_chart(self):
            counts = get_dashboard_counts()
            set_pie_series(self.series, counts)
        
        def update_money_label(self): #Actualiza el dinero recaudado en las facturas al regresar al menú principal
            self.money.setText(str(f"${s.get_total_amount_invoices()}"))

        # Llamar a update_dashboard_chart al mostrar/ocultar frames relevantes
        self.update_dashboard_chart = update_dashboard_chart.__get__(self)
        self.update_dashboard_chart()

        # Llamar a update_money_label al mostrar/ocultar frames relevantes
        self.update_money_label = update_money_label.__get__(self)
        self.update_money_label()


    def createButtons(self):
        button = ButtonFactory()

        # Widget para contener el layout de botones
        self.buttonWidget = QWidget()
        self.buttonLayout = QGridLayout(self.buttonWidget)
        self.buttonLayout.setContentsMargins(2, 2, 2, 2)
        self.buttonLayout.setSpacing(10)
        self.buttonLayout.setAlignment(Qt.AlignBottom | Qt.AlignRight)
        self.dashboardBottomLayout.addWidget(self.buttonWidget)  # Añadir el widget de botones en la fila 2, ocupando 2 columnas

        # BOTONES DE LA SIDEBAR
        self.btn_logout = button.create_button("Cerrar sesión", style="logout", font_size=14, min_size=(0, 0))
        self.sideBottomLayout.addWidget(self.btn_logout, 0, Qt.AlignBottom | Qt.AlignRight)
        self.btn_logout.clicked.connect(self.logout)

        self.btn_ventas = button.create_button("Tus últimas ventas", style="sales", font_size=14, min_size=(200, 0))
        self.btn_ventas.setFixedWidth(200)
        self.sideMidTopLayout.addWidget(self.btn_ventas, 0, 0, Qt.AlignLeft)
        self.btn_ventas.clicked.connect(self.display_ventas)

        self.btn_gestionar_facturas = button.create_button("Gestionar facturas", style = "sales", font_size=14, min_size=(200,0))
        self.sideMidTopLayout.addWidget(self.btn_gestionar_facturas, 1, 0, Qt.AlignLeft)
        self.btn_gestionar_facturas.clicked.connect(self.toggle_invoices_mgmt_frame)

        self.btn_ayuda = button.create_button("Ayuda", style = "sales", font_size=14, min_size=(100,0))
        self.btn_ayuda.setFixedWidth(100)
        self.sideMidTopLayout.addWidget(self.btn_ayuda, 2, 0, Qt.AlignLeft)
        self.btn_ayuda.clicked.connect(self.show_help)

        self.btn_about = button.create_button("Acerca de", style = "sales", font_size=14, min_size=(130,0))
        self.btn_about.clicked.connect(self.about)
        self.btn_about.setFixedWidth(130)
        self.sideMidTopLayout.addWidget(self.btn_about, 3, 0, Qt.AlignLeft)

        self.separador = QLabel(self.sideBar)
        self.separador.setStyleSheet("background-color: transparent;")
        self.separador.setFixedHeight(50)
        self.sideMidTopLayout.addWidget(self.separador, 4, 0)

        # BOTONES DEL DASHBOARD
        self.btn_facturas = button.create_button("Facturas", icon_path="src/assets/icons/Clipboard.png")
        self.buttonLayout.addWidget(self.btn_facturas, 0, 0)
        self.btn_facturas.clicked.connect(self.toggle_create_invoices_frame)

        self.btn_clientes = button.create_button("Clientes", icon_path="src/assets/icons/Briefcase.png")
        self.buttonLayout.addWidget(self.btn_clientes, 0, 1)
        self.btn_clientes.clicked.connect(self.toggle_client_frame)

        self.btn_productos = button.create_button("Productos y servicios", icon_path="src/assets/icons/dollarSign.png")
        self.buttonLayout.addWidget(self.btn_productos, 1, 0)
        self.btn_productos.clicked.connect(self.toggle_products_frame)

        self.btn_salir = button.create_button("Salir", style="exit", icon_path="src/assets/icons/Xsquare.png")
        self.buttonLayout.addWidget(self.btn_salir, 1, 1)
        self.btn_salir.clicked.connect(self.close_window)

        self.btn_settings = button.create_button("", "default_black", "src/assets/icons/settings.png", min_size = (75, 75))
        self.btn_settings.setToolTip("Ajustes")
        self.btn_settings.clicked.connect(self.open_settings)
        self.dashboardHeader.addWidget(self.btn_settings, 0, 3, 2, 2, Qt.AlignTop | Qt.AlignRight)

    def toggle_frame(self, frame_attr, frame_class, back_button_attr, toggle_method, dashboard_elements):
        # Alternar entre el contenido actual y un frame específico
        if not hasattr(self, frame_attr):
            frame_instance = frame_class(self.dashboard)
            setattr(self, frame_attr, frame_instance)
            self.dashboardMidLayout.addWidget(frame_instance)

        if not hasattr(self, back_button_attr):
            button = ButtonFactory()
            back_button = button.create_button("Volver", "back", "src/assets/icons/black-arrow-back.png", 14, (90, 45), Qt.AlignLeft)
            back_button.clicked.connect(toggle_method)
            back_button.setShortcut("Esc")
            setattr(self, back_button_attr, back_button)
            
            # Crear un layout aparte para el botón de volver, debajo del frame correspondiente
            frame_instance = getattr(self, frame_attr)
            self.backButtonLayout = QGridLayout()
            self.backButtonLayout.setAlignment(Qt.AlignBottom | Qt.AlignLeft)
            self.backButtonLayout.addWidget(back_button, 0, 0, Qt.AlignLeft)
            
            # Crear un widget contenedor para el layout del botón de volver
            self.backButtonWidget = QWidget()
            self.backButtonWidget.setLayout(self.backButtonLayout)
            
            # Agregar el widget del botón de volver al layout principal del frame (asumiendo que el frame tiene un layout principal)
            if hasattr(frame_instance, 'layout'):
                frame_instance.layout().addWidget(self.backButtonWidget)

        frame = getattr(self, frame_attr)
        back_button = getattr(self, back_button_attr)

        if frame.isVisible():
            # Limpiar labels de Invoice si corresponde
            if frame_attr == 'invoiceFrame':
                frame.client_details_label.setText("")
                frame.total_amount_label.setText("Total: $0.00")
            # Ocultar el frame y mostrar los elementos originales del dashboard
            frame.setVisible(False)
            back_button.setVisible(False)
            for element in dashboard_elements:
                element.setVisible(True)
            # Actualizar el chart y el label de dinero al volver al dashboard
            self.update_dashboard_chart()
            self.update_money_label()

        else:
            # Mostrar el frame y ocultar los elementos originales del dashboard
            frame.setVisible(True)
            back_button.setVisible(True)
            for element in dashboard_elements:
                element.setVisible(False)
            # Actualizar el chart y el label de dinero al mostrar el frame
            self.update_dashboard_chart()
            self.update_money_label()


    def toggle_client_frame(self):
        from clients import Client
        dashboard_elements = [self.total_label, self.money, self.menu_label, self.res_label, self.btn_settings, self.buttonWidget, self.chart_view, self.chart, self.series]
        self.toggle_frame('clientsFrame', Client, 'clientBackButton', self.toggle_client_frame, dashboard_elements)

    def toggle_products_frame(self):
        from products import Product
        dashboard_elements = [self.total_label, self.money, self.menu_label, self.res_label, self.btn_settings, self.buttonWidget, self.chart_view, self.chart, self.series]
        self.toggle_frame('productsFrame', Product, 'productBackButton', self.toggle_products_frame, dashboard_elements)

    def toggle_create_invoices_frame(self):
        from invoices import Invoice
        dashboard_elements = [self.total_label, self.money, self.menu_label, self.res_label, self.btn_settings, self.buttonWidget, self.chart_view, self.chart, self.series]
        self.toggle_frame('invoiceFrame', Invoice, 'invoiceBackButton', self.toggle_create_invoices_frame, dashboard_elements)
        self.invoiceFrame.update_lists()

    def toggle_invoices_mgmt_frame(self):
        from invoices_mgmt import InvoiceMgmt
        dashboard_elements = [self.total_label, self.money, self.menu_label, self.res_label, self.btn_settings, self.buttonWidget, self.chart_view, self.chart, self.series]

        # Ocultar cualquier otro frame activo antes de mostrar el de gestión de facturas
        frames_attrs = ['clientsFrame', 'productsFrame', 'invoiceFrame']
        for attr in frames_attrs:
            if hasattr(self, attr):
                frame = getattr(self, attr)
                if frame.isVisible():
                    frame.setVisible(False)
        
        # Ocultar también los botones de volver de otros frames si están visibles
        back_buttons = ['clientBackButton', 'productBackButton', 'invoiceBackButton']
        for btn_attr in back_buttons:
            if hasattr(self, btn_attr):
                btn = getattr(self, btn_attr)
                if btn.isVisible():
                   btn.setVisible(False)

        self.toggle_frame('invoicesMgmtFrame', InvoiceMgmt, 'invoicesMgmtBackButton', self.toggle_invoices_mgmt_frame, dashboard_elements)
    
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
    
    def open_settings(self):
        from settings import SettingsWindow
        self.settings_window = SettingsWindow()
        self.settings_window.show()

    def logout(self):
        from login import LoginWindow

        q = MsgBoxFactory()
        response = q.create_question_box("question", "Información", "¿Desea cerrar sesión?", QMessageBox.Information, "Archivo Medium", 12, ["Sí", "No"], [QMessageBox.AcceptRole, QMessageBox.RejectRole])
        response.exec()
        if response.clickedButton().text() == "Sí":  # Verifica si el botón "Sí" fue presionado
            self.close()
            self.login_window = LoginWindow()
            self.login_window.show()

    def display_ventas(self):
        label = LabelFactory()

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
                self.ventasLayout.setAlignment(Qt.AlignCenter)
                self.ventasLayout.setSpacing(50)
                self.sideMidTopLayout.addWidget(self.ventasWidget, 1, 0, Qt.AlignCenter)

                facturas = s.get_last_facturas()[:5]  # Obtener las últimas 5 facturas

                # Mostrar las facturas en etiquetas
                for factura in facturas:
                    factura_label = label.create_label(f"{factura[0]}: {factura[1]}", "Archivo Medium", "medium_white", 12)
                    self.ventasLayout.addWidget(factura_label, Qt.AlignCenter | Qt.AlignTop)
            self.sideMidTopLayout.addWidget(self.ventasWidget)
            self.ventasWidget.setVisible(True)
            
    def initDateTime(self): # Función para mostrar la fecha actual
        now = datetime.now()
        self.date_label.setText(now.strftime("%d/%m/%Y"))
    
    def initUser(self, username, email):
        # Mostrar el usuario que inició sesión
        self.user_label.setText(username)
        self.email_label.setText(email)
    
    def about(self): #Método que muestra información sobre la aplicación
        q = MsgBoxFactory()
        q.resize(400, 200)
        response  = q.about(self, "Acerca de", "Lachmann Invoice Generator for Aqualab Ozono y Salud S.A.S\n\nVersión 1.0\n\nDesarrollado por RossTech Solutions\nBajo licencia GPL")

        return response
    
    def close_window(self):
        self.close()

    def show_help(self):
        from help import HelpWindow
        self.help_window = HelpWindow()
        self.help_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())