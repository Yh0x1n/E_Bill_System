#Aplicación de gestión de inventario utilizando SQL y Pandas

#Importaciones
import pandas as pd, os, sys, random
from PySide6.QtWidgets import QMainWindow, QLabel, QApplication, QInputDialog
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtCore import Qt
import reportlab, qrcode, Crypto

#Clase principal
class MainWindow(QMainWindow): #Aquí van los atributos principales de la ventana
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 640, 480)

        label = QLabel("Holi", self)
        label.setFont(QFont("Roboto", 20))
        label.setGeometry(0, 0, 640, 480)
        label.setStyleSheet("color : blue;"
                            "background-color : gray;")
        label.setAlignment(Qt.AlignCenter)

def main(): #Función principal, donde se inicia el programa al ser llamada
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()