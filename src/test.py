from PySide6.QtWidgets import QApplication, QMainWindow, QToolButton, QPushButton, QVBoxLayout, QFrame, QWidget
from PySide6.QtCore import Qt
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Botón de Hamburguesa con Botones")
        self.setGeometry(100, 100, 800, 600)

        # Crear un widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Crear un layout para el widget central
        layout = QVBoxLayout(central_widget)

        # Crear el botón de hamburguesa
        self.menu_button = QToolButton(self)
        self.menu_button.setText("☰")  # Símbolo de hamburguesa
        self.menu_button.setStyleSheet("""
            QToolButton {
                font-size: 24px;
                background-color: #0078D7;
                color: white;
                border-radius: 5px;
                padding: 10px;
            }
            QToolButton:hover {
                background-color: #005A9E;
            }
        """)
        self.menu_button.clicked.connect(self.toggle_menu)

        # Crear un contenedor para los botones adicionales
        self.menu_frame = QFrame(self)
        self.menu_frame.setStyleSheet("background-color: #f0f0f0; border: 1px solid #ccc;")
        self.menu_frame.setVisible(False)  # Ocultar inicialmente

        # Crear un layout para el contenedor
        menu_layout = QVBoxLayout(self.menu_frame)
        menu_layout.setContentsMargins(10, 10, 10, 10)

        # Añadir botones al contenedor
        btn_home = QPushButton("Inicio", self)
        btn_home.clicked.connect(self.show_home)
        menu_layout.addWidget(btn_home)

        btn_profile = QPushButton("Perfil", self)
        btn_profile.clicked.connect(self.show_profile)
        menu_layout.addWidget(btn_profile)

        btn_settings = QPushButton("Configuración", self)
        btn_settings.clicked.connect(self.show_settings)
        menu_layout.addWidget(btn_settings)

        btn_logout = QPushButton("Cerrar sesión", self)
        btn_logout.clicked.connect(self.logout)
        menu_layout.addWidget(btn_logout)

        # Añadir el botón de hamburguesa y el contenedor al layout principal
        layout.addWidget(self.menu_button, alignment=Qt.AlignTop)
        layout.addWidget(self.menu_frame)

    def toggle_menu(self):
        # Mostrar u ocultar el contenedor de botones
        self.menu_frame.setVisible(not self.menu_frame.isVisible())

    def show_home(self):
        print("Ir a la página de inicio.")

    def show_profile(self):
        print("Ir a la página de perfil.")

    def show_settings(self):
        print("Ir a la página de configuración.")

    def logout(self):
        print("Has cerrado sesión.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())