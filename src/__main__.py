#Aplicación de gestión de inventario utilizando SQL y Pandas

#Importaciones
from PySide6.QtWidgets import QApplication, QMainWindow
import sys
from login import LoginWindow
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.setWindowTitle("FastInvoice")
    window.show()
    sys.exit(app.exec())