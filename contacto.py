import sqlite3  # Importar sqlite3

class Contacto:
    # Constructor
    def __init__(self, nombre, apellido, telefono, email, id_contacto=None):
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.email = email
        self.id_contacto = id_contacto

    # Método privado para conectar a la base de datos
    def _conectar(self):
        conexion = sqlite3.connect("contactos.db")
        cursor = conexion.cursor()
        return conexion, cursor

    # Método privado para cerrar la conexión
    def _cerrar(self, conexion):
        conexion.commit()
        conexion.close()

    # Método para agregar un contacto
    def agregar(self):
        conexion, cursor = self._conectar()
        cursor.execute(
            "INSERT INTO Contactos (nombre, apellido, telefono, email) VALUES (?, ?, ?, ?)",
            (self.nombre, self.apellido, self.telefono, self.email)
        )  # uso ? para prevenir inyecciones SQL

        self.id_contacto = cursor.lastrowid  # genera el id automático
        self._cerrar(conexion)

        conexion, cursor = self._conectar()
        cursor.execute(
            "INSERT INTO Contactos (nombre, apellido, telefono, email) VALUES (?, ?, ?, ?)",
            (self.nombre, self.apellido, self.telefono, self.email)
        )  # uso ? para prevenir inyecciones SQL

        self.id_contacto = cursor.lastrowid  # genera el id automático
        self._cerrar(conexion)
# Método para modificar contactos
    def modificar(self):
        conexion, cursor = self._conectar()
        cursor.execute(
            "UPDATE Contactos SET nombre=?, apellido=?, telefono=?, email=? WHERE id_contacto=?",
            (self.nombre, self.apellido, self.telefono, self.email, self.id_contacto)
        )
        self._cerrar(conexion)

# Método para eliminar contactos
    def eliminar(self):
        conexion, cursor = self._conectar()
        cursor.execute(
            "DELETE FROM Contactos WHERE id_contacto=?",
            (self.id_contacto,)
        )
        self._cerrar(conexion)

# Método para listar todos los contactos
    def listar(self):
        conexion, cursor = self._conectar()
        cursor.execute("SELECT * FROM Contactos")
        contactos = cursor.fetchall()  # trae todos los registros como lista de tuplas
        self._cerrar(conexion)
