"""Script que se encarga de las exportaciones de los datos a CSV y Excel"""

import pandas as pd
from datetime import datetime
from service import s
from PySide6.QtWidgets import QFileDialog, QMessageBox
from PySide6.QtGui import QIcon
import os

class Export:
    """Clase que se encarga de exportar los datos a CSV y Excel"""
    def __init__(self):
        self.msg = QMessageBox()

    def export_data(self, caller):
        # Configura el filtro de archivo solo para Excel
        file_filter = 'Excel Files (*.xlsx)'

        # Muestra un cuadro de diálogo para elegir la ubicación
        file_path = QFileDialog.getSaveFileName(None, 'Exportar', '', file_filter)

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

                # Ejecuta la consulta y obtiene los datos
                df = pd.read_sql(query, s.conn)  # Ensure 's.engine' is a valid SQLAlchemy engine
                filename, ext = os.path.splitext(file_path[0])
                if not ext:
                    ext = '.xlsx'  # Por defecto, siempre exportar como Excel

                # Verifica si el archivo ya existe
                if os.path.exists(filename + ext):
                    # Si el archivo existe, pregunta si se desea sobrescribir
                    overwrite = QMessageBox.question(None, "Archivo existente",
                                                     f"El archivo {filename + ext} ya existe. ¿Desea sobrescribirlo?",
                                                     QMessageBox.Yes | QMessageBox.No)

                    if overwrite == QMessageBox.No:
                        return
                    
                    elif overwrite == QMessageBox.Yes:
                        # Si se elige sobrescribir, elimina el archivo existente
                        os.remove(filename + ext)

                # Exporta a Excel
                df.to_excel(filename + ext, index=False)

                # Mensaje de confirmación
                self.msg.setIcon(QMessageBox.Icon.Information)
                self.msg.setWindowTitle("Información")

                self.msg.setText("Se ha exportado correctamente el archivo")
                self.msg.exec()

        except:
            pass
