"""
Script de inicio de sesión
"""
from PySide6.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QLabel, QLineEdit, QPushButton, QMessageBox, QFrame, QSizePolicy
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QIcon, QFontDatabase, QPainter, QBrush, QPixmap
import sys
from service import s
from window import MainWindow

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FastInvoice - Login")
        self.setFixedSize(640, 480)
        self.setStyleSheet("""background-color: white;""")
        self.initUI()
        self.initLabels()
        self.initButtons()
        self.check_login()

    def initUI(self):
        self.foregrd = QFrame(self)
        self.foregrd.setStyleSheet("""
                                    border-radius: 15px;
                                    background-color: #f0f0f0;
                                    """)
        self.foregrd.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.foregrd.setFixedSize(400, 440)
        self.foregrd.move(125, 20)

        self.loginLayout = QGridLayout(self.foregrd)
        self.loginLayout.setContentsMargins(20, 20, 20, 20)
        self.loginLayout.setSpacing(0)

        self.foregrd.setLayout(self.loginLayout)
    
    def initLabels(self):
        #Creación de los labels
        self.profile_photo = QLabel()
        pixmap = QIcon("src/assets/pictures/AqualabLogo.jpg").pixmap(100, 100)
        circular_pixmap = QPixmap(100, 100)
        circular_pixmap.fill(Qt.transparent)
        painter = QPainter(circular_pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(pixmap))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(0, 0, 100, 100)
        painter.end()
        self.profile_photo.setPixmap(circular_pixmap)
        self.profile_photo.setStyleSheet("""
            background-color: transparent;
            border-radius: 50px;
            border: 2px solid #f0f0f0;
            """)
        self.loginLayout.addWidget(self.profile_photo, 0, 0, 1, 4, Qt.AlignCenter | Qt.AlignTop)

        #Mensaje de bienvenida
        self.welcome_label = QLabel("¡Bienvenido!")
        self.welcome_label.setFont(QFont("Archivo Black", 18))
        self.welcome_label.setStyleSheet("""
                                        color: black;
                                        background-color: transparent;
                                        """)
        self.loginLayout.addWidget(self.welcome_label, 1, 0, 1, 4, Qt.AlignCenter | Qt.AlignTop)

        #Campos de texto

        self.username_label = QLabel("Usuario")
        self.username_label.setFont(QFont("Archivo Medium", 12))
        self.username_label.setStyleSheet("""
                                        color: black;
                                        background-color: transparent;
                                        """)
        self.username_label.setContentsMargins(65, 0, 0, 0)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Ingrese su nombre de usuario")
        self.username_input.setStyleSheet("""
                                        color: black;
                                        background-color: white;
                                        border: 1px solid black;
                                        border-radius: 5px;
                                        """)
        self.username_input.setFont(QFont("Archivo Medium", 12))
        self.username_input.setFixedSize(235, 30)

        self.loginLayout.addWidget(self.username_label, 2, 0, 1, 3, Qt.AlignLeft | Qt.AlignBottom)
        self.loginLayout.addWidget(self.username_input, 3, 0, 1, 4, Qt.AlignCenter | Qt.AlignTop)


        self.email_label = QLabel("Correo Electrónico")
        self.email_label.setFont(QFont("Archivo Medium", 12))
        self.email_label.setStyleSheet("""
                                        color: black;
                                        background-color: transparent;
                                        """)
        self.email_label.setContentsMargins(65, 0, 0, 0)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Ingrese su correo electrónico")
        self.email_input.setStyleSheet("""
                                        color: black;
                                        background-color: white;
                                        border: 1px solid black;
                                        border-radius: 5px;
                                        """)
        
        self.email_input.setFont(QFont("Archivo Medium", 12))
        self.email_input.setFixedSize(235, 30)

        self.loginLayout.addWidget(self.email_label, 4, 0, 1, 4, Qt.AlignLeft | Qt.AlignBottom)
        self.loginLayout.addWidget(self.email_input, 5, 0, 1, 4, Qt.AlignCenter | Qt.AlignTop)

        self.password_label = QLabel("Contraseña")
        self.password_label.setFont(QFont("Archivo Medium", 12))
        self.password_label.setStyleSheet("""
                                        color: black;
                                        background-color: transparent;
                                        """)
        self.password_label.setContentsMargins(65, 0, 0, 0)
        self.password_input = QLineEdit()
        
        self.password_input.setPlaceholderText("Ingrese su contraseña")
        self.password_input.setStyleSheet("""
                                        color: black;
                                        background-color: white;
                                        border: 1px solid black;
                                        border-radius: 5px;
                                        """)
        self.password_input.setFont(QFont("Archivo Medium", 12))
        self.password_input.setFixedSize(235, 30)
        self.password_input.setEchoMode(QLineEdit.Password)

        self.loginLayout.addWidget(self.password_label, 6, 0, 1, 4, Qt.AlignLeft | Qt.AlignBottom)
        self.loginLayout.addWidget(self.password_input, 7, 0, 1, 4, Qt.AlignCenter | Qt.AlignTop)
        
    def initButtons(self):
        #Dos botones de registro e inicio de sesión
        self.btn_login = QPushButton("Iniciar sesión")
        self.btn_login.setFont(QFont("Archivo Medium", 12))
        self.btn_login.setStyleSheet("""
                                        QPushButton {
                                            color: white;
                                            background-color: blue;
                                            border-radius: 15px;
                                            padding: 10px;
                                        }
                                        QPushButton:hover {
                                            background-color: darkblue;
                                        }
                                    """)
        self.btn_login.setFixedSize(150, 40)
        self.loginLayout.addWidget(self.btn_login, 8, 0, 3, 2, Qt.AlignCenter)

        self.btn_register = QPushButton("Registrarse")
        self.btn_register.setFont(QFont("Archivo Medium", 12))
        self.btn_register.setStyleSheet("""
                                        QPushButton {
                                            color: white;
                                            background-color: blue;
                                            border-radius: 15px;
                                            padding: 10px;
                                        }
                                        QPushButton:hover {
                                            background-color: darkblue;
                                        }
                                        """)
        self.btn_register.setFixedSize(150, 40)
        self.loginLayout.addWidget(self.btn_register, 8, 2, 3, 2, Qt.AlignCenter)

    def check_login(self):
        cursor = s.conn.cursor()
        cursor.execute("SELECT * FROM usuario")
        user = cursor.fetchall()

        if user:
            self.btn_login.setEnabled(True)
            self.loginLayout.removeWidget(self.email_label)
            self.email_label.deleteLater()
            self.loginLayout.removeWidget(self.email_input)
            self.email_input.deleteLater()
            
        else:
            self.btn_login.setEnabled(False)
            self.btn_login.setStyleSheet("background-color: gray;"
                                         "color: white;")
        
        self.btn_login.clicked.connect(self.login)
    
    def login(self):
        self.username = self.username_input.text()
        self.password = self.password_input.text()

        conn = s.connect('src/database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuario WHERE username=? AND password=?", (self.username, self.password))
        result = cursor.fetchone()

        if result:
            self.close()
            self.main_window = MainWindow()
            self.main_window.show()
        else:
            self.show_error_message("Error", "Usuario o contraseña incorrectos.")
        conn.close()

    def show_error_message(self, title, message):
        msg_box = QMessageBox(QMessageBox.Warning, title, message)
        msg_box.addButton("Aceptar", QMessageBox.AcceptRole)
        msg_box.setFont(QFont("Archivo Medium", 12))
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: white;
            }
            QMessageBox QLabel {
                color: black;
                font-size: 14px;
            }
            QMessageBox QPushButton {
                background-color: blue;
                color: white;
                border-radius: 5px;
                padding: 5px;
            }
            QMessageBox QPushButton:hover {
                background-color: darkblue;
            }
        """)
        msg_box.exec()

    def register(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())