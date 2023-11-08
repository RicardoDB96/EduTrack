import tkinter as tk
from datetime import date
from tkinter import messagebox
from DB import controller as db
from .add_materia import AddMateriaDialog

class MateriasInfo:

   def __init__(self, root, materias_ui, id):
    self.root = root
    self.materias_ui = materias_ui
    self.subject_id = id
    self.top = tk.Toplevel(self.root)
    self.top.grab_set()

    # Configuracion de la ventana
    self.top.title("Información de la materia")
    self.top.geometry("300x350")
    self.top.resizable(0, 0)

    # Recuperamos la información de la materia según el id que tenemos y el conteo de tareas y tareas terminadas que tiene
    materia = db.db_controller.getSubjectByID(self.subject_id)
    task_count = db.db_controller.getTaskCountFromSubjectByID(self.subject_id)
    complete_task_count = db.db_controller.getCompleteTaskCountFromSubjectByID(self.subject_id)

    # Creación del color y nombre de la materia a la que pertenece la tarea
    subject_frame = tk.Frame(self.top)
    subject_frame.pack(anchor="w")

    # Mostrar el círculo de color
    circle_label = tk.Label(subject_frame, text="●", fg=materia[2], font=('FontAwesome', 40))
    circle_label.pack(side="left")

    # Mostrar el nombre de la materia
    tk.Label(subject_frame, text=materia[1], font=('FontAwesome', 14)).pack(side="left")

    # Estadisticas de tareas
    tk.Label(self.top, text="Tareas totales", font=("FontAwesome", 16, "bold")).pack(anchor="w", padx=8, pady=8)
    tk.Label(self.top, text=task_count, font=("FontAwesome", 14)).pack(anchor="w", padx=8)

    # Estadisticas de tareas
    tk.Label(self.top, text="Tareas completadas", font=("FontAwesome", 16, "bold")).pack(anchor="w", padx=8, pady=8)
    tk.Label(self.top, text=complete_task_count, font=("FontAwesome", 14)).pack(anchor="w", padx=8)

    # Creación del botón para editar la tarea
    self.update_button = tk.Button(self.top, text="Editar", command=lambda: self.editar_tarea(materia), 
                                   bg="#9bb8f5", activebackground="#496fe8", 
                               activeforeground="white", fg="white", font=('FontAwesome', 12, "bold"))
    self.update_button.pack(fill="x", padx=8, pady=8, side="bottom")

    # Creación del botón para eliminar la tarea
    self.delete_button = tk.Button(self.top, text="Eliminar", command=lambda: self.eliminar_materia(self.subject_id), 
                                   bg="red", activebackground="#8B0000", 
                               activeforeground="white", fg="white", font=('FontAwesome', 12, "bold"))
    self.delete_button.pack(fill="x", padx=8, pady=8, side="bottom")

  # Función para editar los datos de una tarea
   def editar_materia(self, materia):
     AddMateriaDialog(self.top, self.materias_ui, materia, self.top)

  # Función para eliminar una tarea
   def eliminar_materia(self, subject_id):
     confirmacion = messagebox.askyesno("Confirmar eliminación", "¿Estás seguro de que quieres eliminar esta materia?\nPerderas toda la información relacionada con la materia, asi como sus tareas")
     if confirmacion:
       db.db_controller.deleteSubjectByID(subject_id)
       self.top.destroy()
       self.materias_ui.update_materias_list()
       self.materias_ui.update_scrollbar()