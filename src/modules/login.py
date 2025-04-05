"""
Script de inicio de sesión
"""
from PySide6.QtWidgets import QApplication, QMainWindow, QGridLayout, QLabel, QLineEdit, QMessageBox, QFrame, QSizePolicy
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QIcon, QPainter, QBrush, QPixmap
import sys
from service import s
from styles.msg_boxes import MsgBoxFactory
from styles.buttons import ButtonFactory
from window import MainWindow

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Lanchmannn - Inicio de sesión")
        self.setWindowIcon(QIcon("src/assets/pictures/AqualabLogo.jpg"))
        self.setFixedSize(640, 480)
        self.setStyleSheet("""background-color: white;""")
        for init_method in (self.initUI, self.initLabels, self.initButtons, self.check_login): #Inicialización de métodos
            init_method()
        
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
                                        padding: 5px;
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
                                        padding: 5px;
                                        """)
        self.email_label.setContentsMargins(65, 0, 0, 0)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Ingrese su correo electrónico")
        self.email_input.setStyleSheet("""
                                        color: black;
                                        background-color: white;
                                        border: 1px solid black;
                                        border-radius: 5px;
                                        padding: 5px;
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
                                        padding: 5px;
                                        """)
        self.password_input.setFont(QFont("Archivo Medium", 12))
        self.password_input.setFixedSize(235, 30)
        self.password_input.setEchoMode(QLineEdit.Password)

        self.loginLayout.addWidget(self.password_label, 6, 0, 1, 4, Qt.AlignLeft | Qt.AlignBottom)
        self.loginLayout.addWidget(self.password_input, 7, 0, 1, 4, Qt.AlignCenter | Qt.AlignTop)
        
    def initButtons(self):
        #Dos botones de registro e inicio de sesión
        button = ButtonFactory()

        self.btn_login = button.create_button("Iniciar sesión", "login/register", None, 12, (150, 40))
        self.loginLayout.addWidget(self.btn_login, 8, 0, 3, 2, Qt.AlignCenter)

        self.btn_register = button.create_button("Registrarse", "login/register", None, 12, (150, 40))
        self.loginLayout.addWidget(self.btn_register, 8, 2, 3, 2, Qt.AlignCenter)

    def check_login(self):

        s.cur.execute("SELECT * FROM usuario")
        user = s.cur.fetchall()

        if user:
            self.btn_login.setEnabled(True)
            self.email_label.hide()
            self.email_input.hide()
            
            self.btn_login.clicked.connect(self.login)
            self.btn_register.clicked.connect(self.back_to_register)
            
            for input in [self.username_input, self.password_input]:
                input.returnPressed.connect(self.login)
            
        else:
            self.btn_login.setEnabled(False)
            self.btn_login.setStyleSheet(self.btn_login.styleSheet() + "QPushButton{background-color: gray;}")
            self.btn_register.clicked.connect(self.register)

    
    def login(self):
        msg = MsgBoxFactory()
        self.username = self.username_input.text()
        self.password = self.password_input.text()

        s.cur.execute("SELECT * FROM usuario WHERE username=? AND password=?", (self.username, self.password))
        result = s.cur.fetchone()

        if result:
            self.close()
            username, email = result[1], result[2]  # Extrae el usuario y el correo electrónico del resultado de la consulta
            self.main_window = MainWindow(username, email)
            self.main_window.show()
        else:
            error_msg = msg.create_msg_box("warning", "Error", "Usuario o contraseña incorrectos.", QMessageBox.Warning, "Archivo Medium", 12, "Aceptar", QMessageBox.AcceptRole)
            error_msg.exec()

    def register(self):
        msg = MsgBoxFactory()
        self.username = self.username_input.text()
        self.email = self.email_input.text()
        self.password = self.password_input.text()

        if not self.username or not self.email or not self.password:
            error_msg = msg.create_msg_box("warning", "Error", "No puede introducir un campo vacío",
                                           QMessageBox.Warning, "Archivo Medium", 12, "Aceptar", QMessageBox.AcceptRole)
            error_msg.exec()
            return

        s.cur.execute("SELECT * FROM usuario WHERE username=? OR email=? OR password=?", (self.username, self.email, self.password))
        result = s.cur.fetchone()

        if result:
            error_msg = msg.create_msg_box("warning", "Error", "Usuario, correo o contraseña ya registrados",
                                           QMessageBox.Warning, "Archivo Medium", 12, "Aceptar", QMessageBox.AcceptRole)
            error_msg.exec()
        else:
            try:
                s.cur.execute("INSERT INTO usuario (username, email, password) VALUES (?, ?, ?);", (self.username, self.email, self.password))
                s.conn.commit()
                success_msg = msg.create_msg_box("information", "Información", "Usuario creado exitósamente.",
                                                 QMessageBox.Information, "Archivo Medium", 12, "Aceptar", QMessageBox.AcceptRole)
                success_msg.exec()

                for input_field in [self.username_input, self.email_input, self.password_input]:
                    input_field.clear()

                for element in [self.email_label, self.email_input]:
                    element.hide()

                if not self.btn_login.isEnabled():
                    self.btn_login.setEnabled(True)
                    self.btn_login.setStyleSheet(self.btn_login.styleSheet() + "QPushButton{background-color: blue}")
                    self.btn_login.clicked.connect(self.login)
                
                else:
                    self.btn_register.clicked.connect(self.back_to_register)

            except Exception as e:
                error_msg = msg.create_msg_box("warning", "Error", f"Error al registrar usuario: {str(e)}",
                                               QMessageBox.Warning, "Archivo Medium", 12, "Aceptar", QMessageBox.AcceptRole)
                error_msg.exec()
    
    def back_to_register(self):
        #Este método hace que el usuario retorne a la pantalla de registro, apareciendo de nuevo el campo de texto de correo electrónico
        self.email_label.show()
        self.email_input.show()
        self.btn_register.clicked.connect(self.register)

def closeEvent(event):
    s.conn.close()
    event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())