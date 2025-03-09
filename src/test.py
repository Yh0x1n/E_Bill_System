from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget
from PySide6.QtGui import QFontDatabase, QFont
import sys
import os

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        font_paths = [
            os.path.abspath("src/fonts/Archivo-Regular.ttf"),
            os.path.abspath("src/fonts/Archivo-Bold.ttf"),
            os.path.abspath("src/fonts/Archivo-Medium.ttf"),
            os.path.abspath("src/fonts/Archivo-Black.ttf")
        ]
        for font_path in font_paths:
            id = QFontDatabase.addApplicationFont(font_path)
            if id < 0: print("Error")
        
        print(QFontDatabase.families())

app = QApplication(sys.argv)
window = MainWindow()
window.show()