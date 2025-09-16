import tkinter as tk
from tkinter import ttk, messagebox
from contacto import Contacto
from factura import Factura

class AppContactos:
    def __init__(self, root): 
        self.root = root
        self.root.title("Gestión de Contactos y Facturas")
        self.root.geometry("700x700") 

        # Variables para los campos del formulario (aca se guarda lo que escribe el user)
        self.nombre_var = tk.StringVar()
        self.apellido_var = tk.StringVar()
        self.telefono_var = tk.StringVar()
        self.email_var = tk.StringVar()

        # fframe para el formulario de alta/modificacion
        frame_form = tk.LabelFrame(root, text="Formulario de Contacto", padx=10, pady=10)
        frame_form.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_form, text="Nombre:").grid(row=0, column=0, sticky="e")
        tk.Entry(frame_form, textvariable=self.nombre_var).grid(row=0, column=1, padx=5)

        tk.Label(frame_form, text="Apellido:").grid(row=1, column=0, sticky="e")
        tk.Entry(frame_form, textvariable=self.apellido_var).grid(row=1, column=1, padx=5)

        tk.Label(frame_form, text="Teléfono:").grid(row=2, column=0, sticky="e")
        tk.Entry(frame_form, textvariable=self.telefono_var).grid(row=2, column=1, padx=5)

        tk.Label(frame_form, text="Email:").grid(row=3, column=0, sticky="e")
        tk.Entry(frame_form, textvariable=self.email_var).grid(row=3, column=1, padx=5)

        # Botones para las acciones CRUD (crear, editar, borrar)
        tk.Button(frame_form, text="Agregar", command=self.agregar_contacto).grid(row=4, column=0, pady=10)
        tk.Button(frame_form, text="Modificar", command=self.modificar_contacto).grid(row=4, column=1, pady=10)
        tk.Button(frame_form, text="Eliminar", command=self.eliminar_contacto).grid(row=4, column=2, pady=10)

        # Tabla donde se muestran todos los contactos 
        frame_tabla = tk.LabelFrame(root, text="Lista de Contactos")
        frame_tabla.pack(fill="both", expand=True, padx=10, pady=5)

        self.tabla = ttk.Treeview(frame_tabla, columns=("ID", "Nombre", "Apellido", "Telefono", "Email"), show="headings")
        self.tabla.heading("ID", text="ID")
        self.tabla.heading("Nombre", text="Nombre")
        self.tabla.heading("Apellido", text="Apellido")
        self.tabla.heading("Telefono", text="Teléfono")
        self.tabla.heading("Email", text="Email")
        self.tabla.pack(fill="both", expand=True)

        #Cuando el user hace click en una fila de la tabla, se cargan esos datos en el form
        self.tabla.bind("<ButtonRelease-1>", self.seleccionar_contacto)

        # Variables para las facturas
        self.monto_var = tk.StringVar()
        self.fecha_var = tk.StringVar()
        self.id_factura = None  # Para controlar factura seleccionada

        # Formulario para información de factura
        frame_factura = tk.LabelFrame(root, text="Gestión de Facturas", padx=10, pady=10)
        frame_factura.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_factura, text="Monto:").grid(row=0, column=0, sticky="e")
        tk.Entry(frame_factura, textvariable=self.monto_var).grid(row=0, column=1, padx=5)

        tk.Label(frame_factura, text="Fecha (YYYY-MM-DD):").grid(row=1, column=0, sticky="e")
        tk.Entry(frame_factura, textvariable=self.fecha_var).grid(row=1, column=1, padx=5)

        tk.Button(frame_factura, text="Agregar", command=self.agregar_factura).grid(row=2, column=0, pady=10)
        tk.Button(frame_factura, text="Modificar", command=self.modificar_factura).grid(row=2, column=1, pady=10)
        tk.Button(frame_factura, text="Eliminar", command=self.eliminar_factura).grid(row=2, column=2, pady=10)

        # Tabla de factura
        frame_tabla_factura = tk.LabelFrame(root, text="Lista de Facturas")
        frame_tabla_factura.pack(fill="both", expand=True, padx=10, pady=5)

        self.tabla_factura = ttk.Treeview(frame_tabla_factura, columns=("ID", "ID Contacto", "Monto", "Fecha"), show="headings")
        self.tabla_factura.heading("ID", text="ID Factura")
        self.tabla_factura.heading("ID Contacto", text="ID Contacto")
        self.tabla_factura.heading("Monto", text="Monto")
        self.tabla_factura.heading("Fecha", text="Fecha")
        self.tabla_factura.pack(fill="both", expand=True)

        self.tabla_factura.bind("<ButtonRelease-1>", self.seleccionar_factura)

        # Cargar contactos y facturas al iniciar la app
        self.listar_contactos()

    # Funciones del CRUD
    def agregar_contacto(self): #Se crea un objeto contacto con la información cargada
        contacto = Contacto(
            self.nombre_var.get(),
            self.apellido_var.get(),
            self.telefono_var.get(),
            self.email_var.get()
        )
        contacto.agregar()
        messagebox.showinfo("Éxito", "Contacto agregado correctamente")
        self.listar_contactos()
        self.limpiar_campos()

    def listar_contactos(self): #Limpiar la tabla para evitar duplicados
        for row in self.tabla.get_children():
            self.tabla.delete(row)
        
        #Conectar a la base y traer los contactos
        contacto = Contacto("", "", "", "")
        conexion, cursor = contacto._conectar()
        cursor.execute("SELECT * FROM Contactos")
        contactos = cursor.fetchall()
        contacto._cerrar(conexion)
        
        #Cargar los contactos en la tabla 
        for c in contactos:
            self.tabla.insert("", "end", values=c)

    def seleccionar_contacto(self, event): #Completar campos al seleccionar la fila
        seleccionado = self.tabla.selection()
        if seleccionado:
            datos = self.tabla.item(seleccionado[0], "values")
            self.id_contacto = datos[0]
            self.nombre_var.set(datos[1])
            self.apellido_var.set(datos[2])
            self.telefono_var.set(datos[3])
            self.email_var.set(datos[4])

            # Actualizo la lista de facturas para el contacto seleccionado
            self.listar_facturas()

    def modificar_contacto(self): #Si no hay selección, no se puede modificar
        if not hasattr(self, "id_contacto"):
            messagebox.showwarning("Atención", "Selecciona un contacto primero")
            return
        #Modificación de datos
        contacto = Contacto(
            self.nombre_var.get(),
            self.apellido_var.get(),
            self.telefono_var.get(),
            self.email_var.get(),
            self.id_contacto
        )
        contacto.modificar()
        messagebox.showinfo("Éxito", "Contacto modificado correctamente")
        self.listar_contactos()
        self.limpiar_campos()

    def eliminar_contacto(self): #Si no hay selección, no se puede modificar
        if not hasattr(self, "id_contacto"):
            messagebox.showwarning("Atención", "Selecciona un contacto para borrar")
            return

        contacto = Contacto("", "", "", "", self.id_contacto)
        contacto.eliminar()
        messagebox.showinfo("Éxito", "Contacto eliminado correctamente")
        self.listar_contactos()
        self.limpiar_campos()

    #Resetear el formulario
    def limpiar_campos(self):
        self.nombre_var.set("")
        self.apellido_var.set("")
        self.telefono_var.set("")
        self.email_var.set("")
        if hasattr(self, "id_contacto"):
            del self.id_contacto

    # CRUD Facturas
    def agregar_factura(self): 
        if not hasattr(self, "id_contacto"):
            messagebox.showwarning("Atención", "Seleccioná primero un contacto para asociarle una factura.")
            return

        try:
            monto = float(self.monto_var.get())
            fecha = self.fecha_var.get().strip()
            if not fecha:
                raise ValueError("Fecha vacía")

            factura = Factura(self.id_contacto, monto, fecha)
            factura.agregar()
            messagebox.showinfo("Éxito", "Factura agregada correctamente.")
            self.listar_facturas()
            self.limpiar_campos_factura()
        except ValueError:
            messagebox.showerror("Error", "Monto inválido o fecha no válida. Verificá los datos ingresados.")

    def listar_facturas(self):
        for row in self.tabla_factura.get_children():
            self.tabla_factura.delete(row)

        if not hasattr(self, "id_contacto"):
            return

        factura = Factura(self.id_contacto, 0, "")
        conexion, cursor = factura._conectar()
        cursor.execute("SELECT * FROM Factura WHERE dni=?", (dni,))
        facturas = cursor.fetchall()
        factura._cerrar(conexion)

        for f in facturas:
            self.tabla_factura.insert("", "end", values=f)

    def seleccionar_factura(self, event):
        seleccionado = self.tabla_factura.selection()
        if seleccionado:
            datos = self.tabla_factura.item(seleccionado[0], "values")
            self.id_factura = datos[0]
            self.monto_var.set(datos[2])
            self.fecha_var.set(datos[3])

    def modificar_factura(self):
        if not hasattr(self, "id_factura") or self.id_factura is None:
            messagebox.showwarning("Atención", "Seleccioná una factura para modificar.")
            return

        try:
            monto = float(self.monto_var.get())
            fecha = self.fecha_var.get().strip()
            if not fecha:
                raise ValueError("Fecha vacía")

            factura = Factura(self.id_contacto, monto, fecha, self.id_factura)
            factura.modificar()
            messagebox.showinfo("Éxito", "Factura modificada correctamente.")
            self.listar_facturas()
            self.limpiar_campos_factura()
        except ValueError:
            messagebox.showerror("Error", "Monto inválido o fecha no válida. Verificá los datos ingresados.")

    def eliminar_factura(self):
        if not hasattr(self, "id_factura") or self.id_factura is None:
            messagebox.showwarning("Atención", "Seleccioná una factura para eliminar.")
            return

        factura = Factura(self.id_contacto, 0, "", self.id_factura)
        factura.eliminar()
        messagebox.showinfo("Éxito", "Factura eliminada correctamente.")
        self.listar_facturas()
        self.limpiar_campos_factura()

    def limpiar_campos_factura(self):
        self.monto_var.set("")
        self.fecha_var.set("")
        self.id_factura = None

if __name__ == "__main__":
    root = tk.Tk()
    app = AppContactos(root)
    root.mainloop()
