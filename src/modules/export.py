"""Script que se encarga de las exportaciones de los datos a CSV y Excel"""

import polars as pl
from datetime import datetime
from service import s
from PySide6.QtWidgets import QFileDialog, QMessageBox, QWidget
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
import os

class Export:
    """Clase que se encarga de exportar los datos a CSV y Excel"""
    def __init__(self):
        self.msg = QMessageBox()

    def export_data(self, caller):
        # Configura el filtro de archivo solo para Excel
        file_filter = 'Excel Files (*.xlsx)'

        # Crear una ventana padre temporal con el ícono
        parent = QWidget()
        parent.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), "../assets/pictures/AqualabLogo.jpg")))
        parent.setWindowTitle("Exportar")
        parent.setAttribute(Qt.WA_DeleteOnClose)
        parent.hide()  # No mostrar la ventana, solo usarla como parent

        # Abre el diálogo para guardar el archivo
        file_path = QFileDialog.getSaveFileName(parent, 'Exportar', '', file_filter)

        try:
            if file_path[0]:  # Verifica si se seleccionó un archivo
                # Determina la consulta según el caller
                queries = {
                    "clients": 'SELECT * FROM cliente;',
                    "products": 'SELECT * FROM producto;'
                }

                query = queries.get(caller)
                if not query:
                    raise ValueError("Caller no reconocido")

                # Ejecuta la consulta y obtiene los datos usando Polars
                df = pl.read_database(query, s.conn)
                filename, ext = os.path.splitext(file_path[0])
                if not ext:
                    ext = '.xlsx'  # Por defecto, siempre exportar como Excel

                # Verifica si el archivo ya existe
                if os.path.exists(filename + ext):
                    # Si el archivo existe, pregunta si se desea sobrescribir
                    overwrite = QMessageBox.question(
                        parent,
                        "Archivo existente",
                        f"El archivo {filename + ext} ya existe. ¿Desea sobrescribirlo?",
                        QMessageBox.Yes | QMessageBox.No
                    )

                    if overwrite == QMessageBox.No:
                        return
                    elif overwrite == QMessageBox.Yes:
                        # Si se elige sobrescribir, elimina el archivo existente
                        os.remove(filename + ext)

                # Exportar a Excel usando Polars
                df.write_excel(filename + ext)

                # Mensaje de confirmación
                self.msg.setIcon(QMessageBox.Icon.Information)
                self.msg.setWindowTitle("Información")
                self.msg.setText("Se ha exportado correctamente el archivo")
                self.msg.exec()
        except Exception:
            pass
