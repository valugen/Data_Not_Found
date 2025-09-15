#Creamos un archivo distinto para crear la tabla de base de datos

import sqlite3

#conectamos
conexion = sqlite3.connect("contactos.db")
cursor = conexion.cursor()

#sentencia DDL para crear tabla
cursor.execute("""
CREATE TABLE IF NOT EXISTS Contactos (
    id_contacto INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL,
    telefono TEXT NOT NULL,
    email TEXT NOT NULL
)
""")

conexion.commit()
conexion.close()

print("Tabla Contactos creada correctamente")
