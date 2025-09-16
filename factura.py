import sqlite3  # Importar sqlite3

class Factura:
    def __init__(self, id_contacto, monto, fecha, id_factura=None):
        self.id_factura = id_factura
        self.id_contacto = id_contacto
        self.monto = monto
        self.fecha = fecha

    # Método privado para conectar la base de datos
    def _conectar(self):
        conexion = sqlite3.connect("contactos.db")
        cursor = conexion.cursor()
        return conexion, cursor

    # Método privado para cerrar conexión
    def _cerrar(self, conexion):
        conexion.commit()
        conexion.close()

    # Método para agregar factura
    def agregar(self):
        conexion, cursor = self._conectar()
        cursor.execute(
            "INSERT INTO Factura (id_contacto, monto, fecha) VALUES (?, ?, ?)",
            (self.id_contacto, self.monto, self.fecha)
        )
        self.id_factura = cursor.lastrowid
        self._cerrar(conexion)
      # uso ? para prevenir inyecciones SQL

    # Método para modificar factura
    def modificar(self):
        conexion, cursor = self._conectar()
        cursor.execute(
            "UPDATE Factura SET id_contacto=?, monto=?, fecha=? WHERE id_factura=?",
            (self.id_contacto, self.monto, self.fecha, self.id_factura)
        )
        self._cerrar(conexion)

    # Método para eliminar factura
    def eliminar(self):
        conexion, cursor = self._conectar()
        cursor.execute(
            "DELETE FROM Factura WHERE id_factura=?",
            (self.id_factura,)
        )
        self._cerrar(conexion)

    # Método para listar facturas
    def listar(self):
        conexion, cursor = self._conectar()
        cursor.execute("SELECT * FROM Factura")
        facturas = cursor.fetchall()
        self._cerrar(conexion)
        return facturas
