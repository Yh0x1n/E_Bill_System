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
                    id_producto TEXT PRIMARY KEY,
                    nombre TEXT NOT NULL,
                    descripcion TEXT NOT NULL,
                    precio INTEGER NOT NULL
                );""") #Tabla "producto"
            
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS cliente (
                    id_cliente TEXT PRIMARY KEY,
                    nombre_cliente TEXT NOT NULL,
                    cedula TEXT NOT NULL,
                    direccion TEXT NOT NULL,
                    telefono TEXT NOT NULL,
                    email TEXT NOT NULL
                );""") #Tabla "cliente"
            
            self.cur.execute("""
            CREATE TABLE IF NOT EXISTS facturas (
                id_factura TEXT PRIMARY KEY,
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

    #Clientes
    def insert_client(self, nombre, cedula, dir, tlf, email):
        import random
        id_cliente = f"CLI-{str(random.randint(100, 999))}"
        self.cur.execute("INSERT INTO cliente(id_cliente, nombre_cliente, cedula, direccion, telefono, email) VALUES (?, ?, ?, ?, ?, ?);", (id_cliente, nombre, cedula, dir, tlf, email))
        return self.conn.commit()

    def delete_client(self, id_cliente):
        self.cur.execute("DELETE FROM cliente WHERE id_cliente = ?;", (id_cliente,))
        return self.conn.commit()

    def edit_client(self):
        self.cur.execute("") #TO-DO: Crear los comandos SQL para la edición de campos
        return self.conn.commit()
    
    def show_client_details(self, id_cliente):
        self.cur.execute("SELECT * FROM cliente WHERE id_cliente = ?;", (id_cliente,))
        return self.cur.fetchall()
        
    #Facturas
    def get_last_facturas(self):
        self.cur.execute("SELECT id_factura FROM facturas ORDER BY id_factura DESC LIMIT 5")
        return self.cur.fetchall()
    
    def close(self): #Cierra la conexión
        self.conn.close()

s = Service()