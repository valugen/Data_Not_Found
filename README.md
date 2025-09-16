# Data_Not_Found
Sistema de ABM de contactos
El proyecto de sistema ABM permite gestionar contactos y registrar facturas asociadas a cada uno, utilizando el 
leguaje de programación Python. Utiliza SQLite como base de datos y Tkinter como interfaz gráfica.

Integrantes:
Gesto, Valentina (41893604)
Herrera, Bruno (46592052)
Theaux, Jimena (40928800)

Contenido del zip.:
- app.py → interfaz gráfica principal con Tkinter
- crear_tabla.py → script para crear las tablas en la base de datos
- contacto.py → clase Contacto (modelo con métodos CRUD)
- factura.py → clase Factura (modelo con métodos CRUD)
- contactos.db → base de datos SQLite
- readme.md → este archivo
- evidencia2.pdf → archivo entregado con información solicitada
- presentacionproyecto.mp4

Requisitos
- Python 3.9 o superior

Módulos estándar: tkinter, sqlite3

Cómo ejecutar
1. Ejecutar crear_tabla.py para crear la base de datos: python crear_tabla.py
2. Ejecutar la interfaz gráfica: python app.py
3. Desde la interfaz agregar/modificar/eliminar contactos y registrar facturas para cada uno.
