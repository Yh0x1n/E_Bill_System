"""
Script que se encarga de realizar la conexión con la base de datos,
así como realizar las consultas necesarias para obtener la información requerida
"""

#Importaciones
import sqlite3 as sql, os, sys

class Service: # Clase que realiza la conexión a la DB
    def __init__(self):
        self.conn = sql.connect(os.path.abspath("src/database.db"))
        self.cur = self.conn.cursor()
        try:
            #Creación de tablas
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS usuario (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    email TEXT NOT NULL,
                    password TEXT NOT NULL,
                    tiempo_creado TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );""") #Tabla "usuario"

            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS producto (
                    id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    descripcion TEXT NOT NULL,
                    precio INTEGER NOT NULL
                );""") #Tabla "producto"
            
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS cliente (
                    id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre_cliente TEXT NOT NULL
                );""") #Tabla "cliente"
            
            self.cur.execute("""
            CREATE TABLE IF NOT EXISTS facturas (
                id_factura INTEGER PRIMARY KEY AUTOINCREMENT,
                numero_factura INTEGER NOT NULL,
                fecha_emision DATE NOT NULL,
                hora_emision TIME NOT NULL,
                id_cliente INTEGER NOT NULL,
                id_producto INTEGER NOT NULL,
                comprobante BLOB NOT NULL,
                emisor INTEGER NOT NULL,
                subtotal INTEGER NOT NULL,
                iva INTEGER NOT NULL,
                total INTEGER NOT NULL,
                FOREIGN KEY (id_cliente) REFERENCES cliente (id_cliente),
                FOREIGN KEY (id_producto) REFERENCES producto (id_producto),
                FOREIGN KEY (emisor) REFERENCES usuario (id)
                );""") #Tabla "facturas"
        
        except sql.Error as e:
            print("Error al crear las tablas: ", e)
            sys.exit(1)

    def get_data(self): #Obtiene todos los datos
        pass

    def get_data_by_id(self, id): #Obtiene los datos por ID
        pass

    def insert_data(self, data): #Inserta datos
        pass

    def update_data(self, data): #Actualiza datos
        pass

    def delete_data(self, id): #Elimina datos
        pass

    def close(self): #Cierra la conexión
        self.conn.close()

s = Service()