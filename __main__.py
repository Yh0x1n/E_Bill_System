#Aplicación de gestión de inventario utilizando MySQL y Pandas

#Importaciones
import sqlite3 as sqlconn
import pandas as pd
import sys
import random
from PySide6 import QtWidgets, QtCore, QtGui
import os

#TO-DO: Empezar a testear las funciones web

#Clase principal
class App(QtWidgets.QWidget): #Esta clase es la ventana principal, que muestra los datos del dataframe al iniciar
    def __init__(self):
        super().__init__()

        #Conectar con la base de datos
        try:
            conn = sqlconn.connect(
                #host = "localhost",
                #user = "root",
                #passwd = "",
                database="inventario"
            )
            cur = conn.cursor()
            #Creando la tabla "productos" con sqlite3
            cur.execute('CREATE TABLE IF NOT EXISTS productos (id INTEGER PRIMARY KEY, nombre TEXT, precio REAL, stock INTEGER);')
            conn.commit()
        
        except sqlconn.Error as e:
            print(e)
        
        #Botones y texto de la ventana
        self.button = QtWidgets.QPushButton("Insertar")
        self.button2 = QtWidgets.QPushButton("Borrar")
        self.button3 = QtWidgets.QPushButton("Actualizar")
        self.button4 = QtWidgets.QPushButton("Salir")
        self.button5 = QtWidgets.QPushButton("Exportar a Excel")

        #Agregando los botones al layout
        self.btn_layout = QtWidgets.QHBoxLayout()
        self.btn_layout.addWidget(self.button, alignment=QtCore.Qt.AlignmentFlag.AlignBottom)
        self.btn_layout.addWidget(self.button2, alignment=QtCore.Qt.AlignmentFlag.AlignBottom)
        self.btn_layout.addWidget(self.button3, alignment=QtCore.Qt.AlignmentFlag.AlignBottom)
        self.btn_layout.addWidget(self.button4, alignment=QtCore.Qt.AlignmentFlag.AlignBottom)
        self.btn_layout.addWidget(self.button5, alignment=QtCore.Qt.AlignmentFlag.AlignBottom)

        #Creando el dataframe
        df = pd.read_sql('SELECT * FROM productos;', conn)
        self.table = QtWidgets.QTableWidget(len(df), len(df.columns))
        self.table.setHorizontalHeaderLabels(df.columns)
        self.table.setVerticalHeaderLabels(df.index)

        #Agregando el dataframe al layout
        self.table_layout = QtWidgets.QVBoxLayout()
        self.table_layout.addWidget(self.table)

        #Ajustando el ancho de columnas fijo del dataframe
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        #Agregando los botones y el dataframe al layout principal
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addLayout(self.btn_layout)
        self.layout.addLayout(self.table_layout)
        self.setLayout(self.layout)

        #Añadiendo color a la ventana
        self.setStyleSheet("background-color: lightgreen;")

        #Añadiendo color a la tabla
        self.table.setStyleSheet("background-color: white;")

        #Añadiendo color a los botones
        self.button.setStyleSheet("background-color: lightblue;")
        self.button2.setStyleSheet("background-color: lightblue;")
        self.button3.setStyleSheet("background-color: lightblue;")
        self.button4.setStyleSheet("background-color: lightblue;")
        self.button5.setStyleSheet("background-color: lightblue;")

        #Conectar los botones con sus respectivas funciones
        self.button.clicked.connect(self.insertar)
        self.button2.clicked.connect(self.borrar)
        self.button3.clicked.connect(self.actualizar)
        self.button4.clicked.connect(self.salir)
        self.button5.clicked.connect(self.exportar)

        #Se actualiza la tabla
        self.actualizar()

    @QtCore.Slot()
    def insertar(self): #Este método despliega una ventana con los campos necesarios para los datos que se deben insertar según la base de datos
        self.dialog = QtWidgets.QInputDialog()

        #Hay tres campos de entrada en la misma ventana (Debo arreglarlo para que se vean todos los campos en una sola ventana)
        text, ok = self.dialog.getText(self, 'Insertar', 'Ingresa el nombre del producto:')
        if ok:
            text2, ok = self.dialog.getText(self, 'Insertar', 'Ingresa el precio del producto:')
            if ok:
                text3, ok = self.dialog.getText(self, 'Insertar', 'Ingresa la cantidad de productos existente:')
                if ok:
                    conn = sqlconn.connect(
                        database = "inventario"
                    )
                    cur = conn.cursor()
                    cur.execute(f'INSERT INTO productos (id, nombre, precio, stock) VALUES ({random.randint(1, 1000)}, "{text}", {text2}, {text3});')
                    conn.commit()

                    #Se actualiza la tabla automáticamente
                    self.actualizar()

    @QtCore.Slot()
    def borrar (self): #Este método borra un producto seleccionado de la base de datos
        conn = sqlconn.connect(
            database = "inventario"
        )
        #Se obtiene el texto del producto al dar clic
        selec = self.table.selectedItems()
        if selec:
            ref = selec[0].text()

            cur = conn.cursor()

            #Salta un cuadro de texto para confirmar la eliminación
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            msg.setWindowTitle("Advertencia")
            msg.setText("¿Estas seguro de borrar este producto?")
            msg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok | QtWidgets.QMessageBox.StandardButton.Cancel)
            msg.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Cancel)
            result = msg.exec()
            if result == QtWidgets.QMessageBox.StandardButton.Ok:
                cur.execute(f'DELETE FROM productos WHERE '
                            f'id = "{ref}"'
                            f'or nombre = "{ref}"'
                            f'or precio = "{ref}"'
                            f'or stock = "{ref}";')
                conn.commit()

            #Se actualiza la tabla automáticamente
            self.actualizar()

    @QtCore.Slot()
    def actualizar (self): #Este método actualiza la tabla automáticamente
        conn = sqlconn.connect(
            database = "inventario"
        )
        df = pd.read_sql('SELECT * FROM productos;', conn)
        self.table.setRowCount(len(df))
        self.table.setColumnCount(len(df.columns))
        self.table.setHorizontalHeaderLabels(df.columns)
        self.table.setVerticalHeaderLabels(df.index)

        for i in range(len(df)):
            for j in range(len(df.columns)):
                self.table.setItem(i, j, QtWidgets.QTableWidgetItem(str(df.iloc[i, j])))
        conn.close()

    @QtCore.Slot()
    def salir (self): #Este método cierra la ventana
        #Sale un mensaje de confirmación
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
        msg.setWindowTitle("Advertencia")
        msg.setText("¿Estas seguro de cerrar la aplicación?\nSe perderán todos los datos no guardados.")
        msg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok | QtWidgets.QMessageBox.StandardButton.Cancel)
        msg.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Cancel)
        result = msg.exec()

        if result == QtWidgets.QMessageBox.StandardButton.Ok:
            sys.exit()
    
    @QtCore.Slot()
    def exportar(self): #Este método exporta la base de datos a un archivo .xlsx, eligiendo dónde guardarlo

        conn = sqlconn.connect(
            database = "inventario"
        )

        #Muestra un cuadro de dialogo para elegir la ubicación
        options = QtWidgets.QFileDialog.getSaveFileName(self, 'Exportar', '', 'Excel Files (*.xlsx)')
        try:
            if options[0]:
                df = pd.read_sql('SELECT * FROM productos;', conn)
                filename, ext = os.path.splitext(options[0])
            if not ext:
                ext = '.xlsx'
            df.to_excel(filename + ext, index=False)

            #Mensaje de confirmación
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
            msg.setWindowTitle("Información")
            msg.setText("Se ha exportado la base de datos")
            msg.exec()
        
        except sqlconn.Error as e:
            msg = QtWidgets.QMessageBox()
            msg.warning(self, 'Error', str(e))
            
        conn.close()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = App()
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec())
