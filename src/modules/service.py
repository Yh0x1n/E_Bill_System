"""
Script que se encarga de realizar la conexión con la base de datos,
así como realizar las consultas necesarias para obtener la información requerida
"""

#Importaciones
import sqlite3 as sql, os, sys

class Service: # Clase que realiza la conexión a la DB
    def __init__(self):
        try:
            db_path = os.path.abspath("src/database.db")
            if not os.path.exists(db_path):
                print(f"La base de datos no se encontró en la ruta: {db_path}\nCreando la base de datos en la ruta especificada...")
                self.conn = sql.connect(db_path)
            else:
                self.conn = sql.connect(db_path)
            self.cur = self.conn.cursor()
            print("Conexión a la base de datos establecida correctamente.")
        except FileNotFoundError as fnf_error:
            print(fnf_error)
            raise

        except sql.Error as db_error:
            print(f"Error al conectar con la base de datos: {db_error}")
            raise

        try:
            #Creación de tablas
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS usuario (
                    id TEXT PRIMARY KEY,
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
                    precio REAL NOT NULL
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
                id_cliente TEXT NOT NULL,
                id_producto TEXT NOT NULL,
                comprobante BLOB NOT NULL,
                emisor TEXT NOT NULL,
                subtotal REAL NOT NULL,
                iva REAL NULL,
                total REAL NOT NULL,
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

    def edit_client(self, id_cliente, nombre, cedula, dir, tlf, email):
        fields = {
            "nombre_cliente": nombre,
            "cedula": cedula,
            "direccion": dir,
            "telefono": tlf,
            "email": email
        }
        set_clause = []
        params = {}
        
        for column, value in fields.items():
            if value is not None and value != "":
                set_clause.append(f"{column} = :{column}")
                params[column] = value

        if not set_clause:
            return

        params["id_cliente"] = id_cliente
        query = f"UPDATE cliente SET {', '.join(set_clause)} WHERE id_cliente = :id_cliente"
        self.cur.execute(query, params)

        return self.conn.commit()
    
    def show_client_details(self, id_cliente):
        self.cur.execute("SELECT * FROM cliente WHERE id_cliente = ?;", (id_cliente,))
        return self.cur.fetchall()

    def get_client_by_id(self):
        self.cur.execute("SELECT id_cliente, nombre_cliente FROM cliente;")
        return self.cur.fetchall()

    #Productos y servicios
    def insert_product(self, nombre, descripcion, precio):
        import random
        # Se utiliza el "codigo" como identificador único (id_producto)
        codigo = f"PRD-{random.randint(100, 999)}"
        try:
            self.cur.execute(
                "INSERT INTO producto(id_producto, nombre, descripcion, precio) VALUES (?, ?, ?, ?)",
                (codigo, nombre, descripcion, precio,)
            )
            self.conn.commit()
        except Exception as e:
            print("Error al insertar el producto:", e)

    def edit_product(self, product_id, nombre, precio, descripcion):
        #TO-DO: ACTUALIZAR ESTE MÉTODO
        fields = {
            "nombre": nombre,
            "precio": precio,
            "descripcion": descripcion
        }
        set_clause = []
        params = {}
        
        for column, value in fields.items():
            if value is not None and value != "":
                set_clause.append(f"{column} = :{column}")
                params[column] = value

        if not set_clause:
            return

        params["id_producto"] = product_id
        query = f"UPDATE producto SET {', '.join(set_clause)} WHERE id_producto = :id_producto"
        self.cur.execute(query, params)

        return self.conn.commit()

    def delete_product(self, product_id):
        try:
            self.cur.execute("DELETE FROM producto WHERE id_producto = ?", (product_id,))
            self.conn.commit()
        
        except Exception as e:
            print("Error al eliminar el producto:", e)

    def show_product_details(self, product_id):
        # Se retorna una tupla con: ID, Nombre, Código, Precio y Descripción

        self.cur.execute("SELECT * FROM producto WHERE id_producto = ?",(product_id,))
        return self.cur.fetchall()

    #Facturas
    def insert_invoice(self, id_factura, fecha_emision, id_cliente, id_producto, comprobante, emisor, subtotal, iva, total):
        try:
            self.cur.execute(
                "INSERT INTO facturas(id_factura, fecha_emision, id_cliente, id_producto, comprobante, emisor, subtotal, iva, total) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (id_factura, fecha_emision, id_cliente, id_producto, comprobante, emisor, subtotal, iva, total)
            )
            self.conn.commit()
        except Exception as e:
            print("Error al insertar la factura:", e)

    def get_last_facturas(self):
        self.cur.execute("""
            SELECT f.id_factura, c.nombre_cliente
            FROM facturas f
            JOIN cliente c ON f.id_cliente = c.id_cliente
            ORDER BY f.id_factura DESC
            LIMIT 5
        """)
        return self.cur.fetchall()

    def edit_user(self, user_id, username, email):
        #TO-DO: ACTUALIZAR ESTE MÉTODO
        fields = {
            "username": username,
            "email": email
        }
        set_clause = []
        params = {}
        
        for column, value in fields.items():
            if value is not None and value != "":
                set_clause.append(f"{column} = :{column}")
                params[column] = value

        if not set_clause:
            return

        params["id"] = user_id
        query = f"UPDATE usuario SET {', '.join(set_clause)} WHERE id = :id"
        self.cur.execute(query, params)
    
    def show_user_details(self, user_id):
        self.cur.execute("SELECT * FROM usuario where id = ?", user_id)
        return self.cur.fetchall()
    
    def close(self): #Cierra la conexión
        if self.conn:
            self.conn.close()
            print("Conexión a la base de datos cerrada correctamente.")


s = Service()