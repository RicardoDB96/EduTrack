import tkinter as tk
from tkinter import colorchooser
from tkinter import messagebox
from DB import controller as db
import sqlite3 as sql

class AddMateriaDialog:

    def __init__(self, root, materias_ui, materia_info, destroy_info):
        self.root = root
        self.materias_ui = materias_ui
        self.top = tk.Toplevel(self.root)
        self.top.grab_set()

        # Configuracion de la ventana
        self.top.title("Agregar Materia")
        self.top.geometry("300x180")
        self.top.resizable(0, 0)

        n_font = ("FontAwesome", 12)

        # Nombre del sistema
        tk.Label(self.top, text="Agregar materia", font=("FontAwesome", 16, "bold")).pack(side="top", fill="x", padx=8, pady=12)

        # Configuración de la fila con los elementos del nombre
        nombre_frame = tk.Frame(self.top)
        nombre_frame.pack(fill="x")
        self.nombre_label = tk.Label(nombre_frame, text="Materia:", font=n_font)
        self.nombre_label.pack(side="left", padx=8)
        self.nombre_entry = tk.Entry(nombre_frame, font=n_font)
        self.nombre_entry.pack(side="right", fill="x", expand=True, padx=8)

         # Configuración de la fila con los elementos del nombre
        color_frame = tk.Frame(self.top)
        color_frame.pack(fill="x", pady=4)
        self.color_label = tk.Label(color_frame, text="Color:    ", font=n_font)
        self.color_label.pack(side="left", padx=8)
        self.color_button = tk.Button(color_frame, text="Elegir Color", command=self.choose_color, font=n_font)
        self.color_button.pack(side="right", fill="x", expand=True, padx=8)

        # Creación del botón para crear la materia
        self.add_button = tk.Button(self.top, text="Agregar", command=self.add_materia, bg="#496fe8", activebackground="#2b3fca", 
                                   activeforeground="white", fg="white", font=('FontAwesome', 12, "bold"))
        self.add_button.pack(fill="x", padx=16, pady=8)

        # Si tenemos información de una materia, procedemos a reflejar dicha información en la UI
        if materia_info != None:
            nombre_materia = materia_info[1]
            color_materia = materia_info[2]

            # ID de la materia
            self.subject_id = materia_info[0]

            self.nombre_entry.insert(0, nombre_materia)
            self.color_button.config(bg=color_materia)

            self.add_button.config(text="Guardar", command=lambda: self.edit_materia(destroy_info))

    # Función para elegir el color de la materia
    def choose_color(self):
        color_code = colorchooser.askcolor(title="Elegir color")[1]
        self.color_button.configure(bg=color_code)
        self.color_button.configure(fg=get_font_color(color_code))# Actualizamos el color de la letra dependiendo el color del background
        self.top.deiconify()

     # Función para añadir la materia en la base de datos y actulizarla
    def edit_materia(self, destroy):
        nombre = self.nombre_entry.get()
        color = self.color_button.cget("bg")

        # Checamos errores
        case = self.check_errors(color, self.top.cget('bg'))

        # Si no tenemos errores, procedemos a ingresar los datos a la base de datos
        if case:
            try:
                db.db_controller.updateSubject(self.subject_id, nombre, color)
                self.top.destroy()
                destroy.destroy()
                self.materias_ui.update_materias_list()
                self.materias_ui.update_scrollbar()
            except sql.IntegrityError as e:
                messagebox.showerror('Error al añadir', 'No se puede añadir una materia con el mismo nombre')

    # Función para añadir la materia en la base de datos y actulizarla
    def add_materia(self):
        nombre = self.nombre_entry.get()
        color = self.color_button.cget("bg")

        # Checamos errores
        case = self.check_errors(color, self.top.cget('bg'))

        # Si no tenemos errores, procedemos a ingresar los datos a la base de datos
        if case:
            try:
                db.db_controller.insertSubject(nombre, color)
                self.top.destroy()
                self.materias_ui.update_materias_list()
                self.materias_ui.update_scrollbar()
            except sql.IntegrityError as e:
                messagebox.showerror('Error al añadir', 'No se puede añadir una materia con el mismo nombre')

    # Funcion para checar los posibles errores al crear una materia
    def check_errors(self, color_code, invalid_color):
        if not self.nombre_entry.get() and color_code == invalid_color:
            messagebox.showerror('Error al añadir', 'Ingrese un texto y seleccione un color')
            return False  # Ambos campos están vacíos
        elif not self.nombre_entry.get():
            messagebox.showerror('Error al añadir', 'Ingrese un texto')
            return False  # Falta el nombre de la materia
        elif color_code == invalid_color:
            messagebox.showerror('Error al añadir', 'Seleccione un color')
            return False  # Falta el color de la materia
        else:
            return True  # No hay errores

# Función para decidir si usar el color blanco o negro segun el color dado
def get_font_color(bg_color):
    r, g, b = (int(bg_color[1:3], 16), int(bg_color[3:5], 16), int(bg_color[5:7], 16))
    return "#000000" if (r * 0.299 + g * 0.587 + b * 0.114) > 186 else "#FFFFFF"