#Creamos un archivo distinto para crear la tabla de base de datos
import sqlite3
#Conectamos
conexion = sqlite3.connect("contactos.db")
cursor = conexion.cursor()

#sentencia DDL para crear tabla contactos
cursor.execute("""
CREATE TABLE IF NOT EXISTS Contactos (
    dni TEXT PRIMARY KEY,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL,
    telefono TEXT NOT NULL,
    email TEXT NOT NULL
)
""")

#sentencia DDL para crear tabla factura
cursor.execute("""
CREATE TABLE IF NOT EXISTS Factura (
    id_factura INTEGER PRIMARY KEY AUTOINCREMENT,
    dni TEXT NOT NULL,
    monto REAL NOT NULL,
    fecha TEXT NOT NULL,
    FOREIGN KEY (dni) REFERENCES Contactos (dni)
)
""")

conexion.commit()
conexion.close()

print("Tablas Contactos y Factura creadas correctamente")
