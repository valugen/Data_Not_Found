import tkinter as tk
from tkinter import ttk, messagebox
from contacto import Contacto


class AppContactos:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion de Contactos")
        self.root.geometry("700x500")

        # variables para los campos del formulario (aca se guarda lo que escribe el user))
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

        # botoncitos para las acciones CRUD (crear, editar, borrar)
        tk.Button(frame_form, text="Agregar", command=self.agregar_contacto).grid(row=4, column=0, pady=10)
        tk.Button(frame_form, text="Modificar", command=self.modificar_contacto).grid(row=4, column=1, pady=10)
        tk.Button(frame_form, text="Eliminar", command=self.eliminar_contacto).grid(row=4, column=2, pady=10)

        # babla donde se muestran todos los contactos (como una lista grande)
        frame_tabla = tk.LabelFrame(root, text="Lista de Contactos")
        frame_tabla.pack(fill="both", expand=True, padx=10, pady=5)

        self.tabla = ttk.Treeview(frame_tabla, columns=("ID", "Nombre", "Apellido", "Telefono", "Email"), show="headings")
        self.tabla.heading("ID", text="ID")
        self.tabla.heading("Nombre", text="Nombre")
        self.tabla.heading("Apellido", text="Apellido")
        self.tabla.heading("Telefono", text="Teléfono")
        self.tabla.heading("Email", text="Email")
        self.tabla.pack(fill="both", expand=True)

        # cuando el user hace click en una fila de la tabla, se cargan esos datos en el form
        self.tabla.bind("<ButtonRelease-1>", self.seleccionar_contacto)

        # apenas abre la app, cargamos tods los contactos
        self.listar_contactos()

    # funciones basicas CRUD
    def agregar_contacto(self):
        # creamos un obj contacto con lo que puso el usuario
        contacto = Contacto(
            self.nombre_var.get(),
            self.apellido_var.get(),
            self.telefono_var.get(),
            self.email_var.get()
        )
        contacto.agregar()
        messagebox.showinfo("Exito", "Contacto agregado correctamente")
        self.listar_contactos()
        self.limpiar_campos()

    def listar_contactos(self):
        # limpiar la tabla primero para no dupliicar cosas
        for row in self.tabla.get_children():
            self.tabla.delete(row)

        # aca usamos el metodo listar del modelo
        contacto = Contacto("", "", "", "")
        conexion, cursor = contacto._conectar()
        cursor.execute("SELECT * FROM Contactos")
        contactos = cursor.fetchall()
        contacto._cerrar(conexion)

        # metemos cada conacto en la tabla
        for c in contactos:
            self.tabla.insert("", "end", values=c)

    def seleccionar_contacto(self, event):
        # cuando el user selecciona una fila, llenamos el form con esos datos
        seleccionado = self.tabla.selection()
        if seleccionado:
            datos = self.tabla.item(seleccionado[0], "values")
            self.id_contacto = datos[0]
            self.nombre_var.set(datos[1])
            self.apellido_var.set(datos[2])
            self.telefono_var.set(datos[3])
            self.email_var.set(datos[4])

    def modificar_contacto(self):
        # si no hay nada seleccionado, no se puede modificar
        if not hasattr(self, "id_contacto"):
            messagebox.showwarning("Atencion", "Selecciona un contacto primero")
            return

        # creamos el obj con los nuevos datos y lo mandamos a modificar
        contacto = Contacto(
            self.nombre_var.get(),
            self.apellido_var.get(),
            self.telefono_var.get(),
            self.email_var.get(),
            self.id_contacto
        )
        contacto.modificar()
        messagebox.showinfo("Exito", "Contacto modificado correctamente")
        self.listar_contactos()
        self.limpiar_campos()

    def eliminar_contacto(self):
        # idem qu arriba, hay q tener un contacto selecccionado
        if not hasattr(self, "id_contacto"):
            messagebox.showwarning("Atencion", "Selecciona un contacto para borrar")
            return

        contacto = Contacto("", "", "", "", self.id_contacto)
        contacto.eliminar()
        messagebox.showinfo("Exito", "Contacto eliminado correctamente")
        self.listar_contactos()
        self.limpiar_campos()

    def limpiar_campos(self):
        # reseteamos el formulario, queda limpio para usar otra vez
        self.nombre_var.set("")
        self.apellido_var.set("")
        self.telefono_var.set("")
        self.email_var.set("")
        if hasattr(self, "id_contacto"):
            del self.id_contacto


if __name__ == "__main__":
    root = tk.Tk()
    app = AppContactos(root)
    root.mainloop()
#fijense que este todo bien, estuve revisando el otro codigo para ver mas o menos q hacer xd
