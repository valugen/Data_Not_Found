#Creamos un archivo distinto para crear la tabla de base de datos

import sqlite3

#conectamos
conexion = sqlite3.connect("contactos.db")
cursor = conexion.cursor()

#sentencia DDL para crear tabla contactos
cursor.execute("""
CREATE TABLE IF NOT EXISTS Contactos (
    id_contacto INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL,
    telefono TEXT NOT NULL,
    email TEXT NOT NULL
)
""")

#sentencia DDL para crear tabla contactos
cursor.execute("""
CREATE TABLE IF NOT EXISTS Factura (
    id_factura INTEGER PRIMARY KEY AUTOINCREMENT,
    id_contacto INTEGER NOT NULL,
    monto REAL NOT NULL,
    fecha TEXT NOT NULL,
    FOREIGN KEY (id_contacto) REFERENCES Contactos (id_contacto)
)
""")

conexion.commit()
conexion.close()

print("Tabla Contactos creada correctamente")

