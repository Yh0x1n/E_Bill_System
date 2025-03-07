'''
Script de la ventana principal de la aplicación
'''
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QStatusBar, QHBoxLayout, QMainWindow, QMenuBar, QMenu, QPushButton, QWidgetAction, QMessageBox, QFrame, QStackedWidget, QSizePolicy
from PySide6.QtCore import QTimer, Qt, QPoint, QSize, QRect
from PySide6.QtGui import QIcon, QAction, QPixmap, QPainter, QBrush
import sys
from datetime import datetime


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("src/assets/AqualabLogo.jpg"))
        self.initUI()
        self.initDateTime()
    
    def initUI(self):
        self.resize(1024, 600)
        self.setWindowTitle("Aqualab")

        self.sideBar = QFrame(self)
        self.sideBar.setFixedSize(300, 600)
        self.sideBar.setStyleSheet("background-color: blue;")

        self.date_label = QLabel(self.sideBar) #Etiqueta para mostrar la fecha
        self.date_label.setStyleSheet("font-size: 14px;"
                          "color: white;")
        self.date_label.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        self.date_label.setGeometry(175, 500, 100, 30)
        """self.date_label.setGeometry(self.sideBar.width() - 120, self.sideBar.height() - 75, 100, 30)"""

        # Etiqueta para mostrar la foto de perfil del usuario
        self.profile_pic = QLabel(self.sideBar)
        self.profile_pic.setStyleSheet("background-color: white;"
                           "border-radius: 35px;")
        self.profile_pic.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.profile_pic.setGeometry(20, 20, 75, 75)
        self.setRoundedProfilePic("src/assets/AqualabLogo.jpg")

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

    def initDateTime(self): #Función para mostrar la fecha actual
        now = datetime.now()
        self.date_label.setText(now.strftime("%d/%m/%Y"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())