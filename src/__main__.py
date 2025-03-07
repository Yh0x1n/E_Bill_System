#Aplicación de gestión de inventario utilizando SQL y Pandas

#Importaciones
from PySide6.QtWidgets import QApplication, QMainWindow
import sys
from window import MainWindow
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("FastInvoice")
    window.show()
    sys.exit(app.exec())