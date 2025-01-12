#Aplicación de gestión de inventario utilizando SQL y Pandas

#Importaciones
import sqlite3 as sql, pandas as pd, os, sys, random
from PySide6 import QtWidgets, QtCore, QtGui
import reportlab, qrcode, Crypto

#Clase principal
class App(QtWidgets.QWidget): #Esta clase es la ventana principal, que muestra los datos del dataframe al iniciar
    def __init__(self):
        super().__init__()

        #Conectar con la base de datos
        try:
            conn = sql.connect(
                #host = "localhost",
                #user = "root",
                #passwd = "",
                database="inventario"
            )
            cur = conn.cursor()
            #Creando la tabla "productos" con sqlite3
            cur.execute('CREATE TABLE IF NOT EXISTS productos (id INTEGER PRIMARY KEY, nombre TEXT, precio REAL, stock INTEGER);')
            conn.commit()
        
        except sql.Error as e:
            print(e)