import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
from DB import controller as db
import sqlite3 as sql

class AddTareaDialog:

  def __init__(self, root, tareas_ui, tarea_info, destroy_info_UI):
    self.root = root
    self.tareas_ui = tareas_ui
    self.top = tk.Toplevel(self.root)
    self.top.grab_set()

    # Configuracion de la ventana
    self.top.title("Agregar Tarea")
    self.top.geometry("300x300")
    self.top.resizable(0, 0)

    n_font = ("FontAwesome", 12)

    # Nombre de la ventana
    tk.Label(self.top, text="Agregar tarea", font=("FontAwesome", 16, "bold")).pack(side="top", fill="x", padx=8, pady=12)

    # Configuración de la fila con los elementos de la tarea
    tarea_frame = tk.Frame(self.top, pady=4)
    tarea_frame.pack(fill="x")
    self.tarea_label = tk.Label(tarea_frame, text="Tarea:    ", font=n_font)
    self.tarea_label.pack(side="left", padx=8)
    self.tarea_entry = tk.Entry(tarea_frame, font=n_font)
    self.tarea_entry.pack(side="right", fill="x", expand=True, padx=8)

    # Configuración de las opciones de la materia
    options = db.db_controller.getAllSubjectNames()
    self.subject = tk.StringVar(self.top)
    self.subject.set("")

    # Configuración de la lista de seleccionar materia
    materia_frame = tk.Frame(self.top, pady=4)
    materia_frame.pack(fill="x")
    self.materia_label = tk.Label(materia_frame, text="Materia:", font=n_font)
    self.materia_label.pack(side="left", padx=8)
    self.materias = tk.OptionMenu(materia_frame, self.subject, *options)
    self.materias.pack(side="right", fill="x", expand=True, padx=8)

    # Función para obtener la fecha seleccionada
    def selected_date():
      date = self.cal.get_date()
      return date.strftime("%d-%m-%Y")

    # Configuración para la selección de fecha
    date_frame = tk.Frame(self.top, pady=4)
    date_frame.pack(fill="x")
    self.date_label = tk.Label(date_frame, text="Entrega:", font=n_font)
    self.date_label.pack(side="left", padx=8)
    self.cal = DateEntry(date_frame, width=12, background='darkblue', foreground='white', borderwidth=2, year=2023)
    self.cal.pack(side="right", fill="x", expand=True, padx=8)

    # Configuración de las opciones de los tipos de tareas
    options = ["Tarea", "Trabajo en Equipo", "Proyecto", "Examen"]
    self.m_type = tk.StringVar(self.top)
    self.m_type.set("")

    # Configuración de la lista de seleccionar el tipo de tarea
    type_frame = tk.Frame(self.top, pady=4)
    type_frame.pack(fill="x")
    self.type_label = tk.Label(type_frame, text="Tipo:      ", font=n_font)
    self.type_label.pack(side="left", padx=8)
    self.type = tk.OptionMenu(type_frame, self.m_type, *options)
    self.type.pack(side="right", fill="x", expand=True, padx=8)

    # Creación del botón para crear la tarea
    self.add_button = tk.Button(self.top, text="Agregar", command=self.add_tarea, bg="#496fe8", activebackground="#2b3fca", 
                               activeforeground="white", fg="white", font=('FontAwesome', 12, "bold"))
    self.add_button.pack(fill="x", padx=16, pady=8)

    # Si tenemos información de una tarea, procedemos a reflejar dicha información en la UI
    if tarea_info != None:
      nombre_tarea = tarea_info[0]
      materia_tarea = tarea_info[1]
      fecha_tarea = tarea_info[3]
      tipo_tarea = tarea_info[4]
      
      # ID de la tarea
      self.task_id = tarea_info[7]

      # Separa el año, mes y día
      year, month, day = fecha_tarea.split("-")

      # Reorganiza los componentes de fecha en el formato deseado
      correct_date = f"{month}-{day}-{year}"

      self.tarea_entry.insert(0, nombre_tarea)
      self.subject.set(materia_tarea)
      self.cal.set_date(correct_date)
      self.m_type.set(tipo_tarea)

      self.add_button.config(text="Guardar", command=lambda: self.edit_tarea(destroy_info_UI))

  # Función para editar la tarea y guardar la nueva información en la DB
  def edit_tarea(self, destroy):
    # Obtenemos todos los valores a ingresar a la DB
    tarea = self.tarea_entry.get()
    date = self.cal.get_date().strftime("%Y-%m-%d")
    mtype = self.m_type.get()

    # Checamos errores
    case = self.check_errors(tarea, self.subject.get(), date, mtype)

    subject = self.subject.get().replace("(", "").replace(",)", "").replace("'", "")

        # Si no tenemos errores, procedemos a ingresar los datos a la base de datos
    if case:
      try:
        materia = db.db_controller.getSubjectID(subject)[0] # Buscamos el id de la materia
        db.db_controller.updateTask(tarea, materia, date, mtype,self.task_id)
        self.top.destroy()
        destroy.destroy()
        self.tareas_ui.update_tareas_list()
        self.tareas_ui.update_scrollbar()
      except sql.OperationalError as e:
        messagebox.showerror('Error al actualizar', e)

  # Función para añadir la tarea en la base de datos y actulizarla
  def add_tarea(self):
    # Obtenemos todos los valores a ingresar a la DB
    tarea = self.tarea_entry.get()
    date = self.cal.get_date().strftime("%Y-%m-%d")
    mtype = self.m_type.get()

    # Checamos errores
    case = self.check_errors(tarea, self.subject.get(), date, mtype)

    subject = self.subject.get().replace("(", "").replace(",)", "").replace("'", "")

    # Si no tenemos errores, procedemos a ingresar los datos a la base de datos
    if case:
      try:
        materia = db.db_controller.getSubjectID(subject)[0] # Buscamos el id de la materia
        db.db_controller.insertTask(tarea, materia, date, mtype)
        self.top.destroy()
        self.tareas_ui.update_tareas_list()
        self.tareas_ui.update_scrollbar()
      except sql.OperationalError as e:
        messagebox.showerror('Error al añadir', e)
    
  # Funcion para checar los posibles errores al crear una materia
  def check_errors(self, tarea, materia, date, type):
    if (tarea == "" or materia == "" or date == "" or type == ""):
      messagebox.showerror('Error al añadir', 'Ingrese los datos para la tarea')
      return False  # Algun campo esta vacio
    else:
      return True  # No hay