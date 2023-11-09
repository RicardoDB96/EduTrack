import tkinter as tk
from datetime import date
from tkinter import messagebox
from DB import controller as db
from .add_tarea import AddTareaDialog

class TareasInfo:

  def __init__(self, root, tareas_ui, id):
    self.root = root
    self.tareas_ui = tareas_ui
    self.task_id = id
    self.top = tk.Toplevel(self.root)
    self.top.grab_set()

    # Configuracion de la ventana
    self.top.title("Información de la tarea")
    self.top.geometry("300x500")
    self.top.resizable(0, 0)

    # Recuperamos la información de la tarea según el id que tenemos
    tarea = db.db_controller.getTaskByID(self.task_id)

    # Nombre de la tarea
    tk.Label(self.top, text=tarea[0], font=("FontAwesome", 16, "bold")).pack(side="top", anchor="w", padx=8)

    # Creación del color y nombre de la materia a la que pertenece la tarea
    subject_frame = tk.Frame(self.top)
    subject_frame.pack(anchor="w")

    # Mostrar el círculo de color
    circle_label = tk.Label(subject_frame, text="●", fg=tarea[2], font=('FontAwesome', 40))
    circle_label.pack(side="left")

    # Mostrar el nombre de la materia
    tk.Label(subject_frame, text=tarea[1], font=('FontAwesome', 14)).pack(side="left")

    # Creación de fechas
    tk.Label(self.top, text="Fecha de entrega", font=("FontAwesome", 16, "bold")).pack(anchor="w", padx=8, pady=8)
    tk.Label(self.top, text=tarea[3], font=("FontAwesome", 14)).pack(anchor="w", padx=8)
    if tarea[5] != 0 and tarea[6] != None:
      tk.Label(self.top, text=f"Completado el {tarea[6]}", font=("FontAwesome", 14)).pack(anchor="w", padx=8)

    tk.Label(self.top, text="Tipo de tarea", font=("FontAwesome", 16, "bold")).pack(anchor="w", padx=8, pady=8)
    tk.Label(self.top, text=tarea[4], font=("FontAwesome", 14)).pack(anchor="w", padx=8)

    # Logica para cambiar el texto
    if tarea[5] != 0:
      complete_text = "Sin completar"
    else:
      complete_text = "Completada"

    # Creación del botón para completar la tarea
    self.complete_button = tk.Button(self.top, text=complete_text, command=lambda: self.completar_tarea(self.task_id, tarea[5]), 
                                     bg="#496fe8", activebackground="#2b3fca", 
                               activeforeground="white", fg="white", font=('FontAwesome', 12, "bold"))
    self.complete_button.pack(fill="x", padx=8, pady=8, side="bottom")

    # Creación del botón para editar la tarea
    self.update_button = tk.Button(self.top, text="Editar", command=lambda: self.editar_tarea(tarea), 
                                   bg="#9bb8f5", activebackground="#496fe8", 
                               activeforeground="white", fg="white", font=('FontAwesome', 12, "bold"))
    self.update_button.pack(fill="x", padx=8, pady=8, side="bottom")

    # Creación del botón para eliminar la tarea
    self.delete_button = tk.Button(self.top, text="Eliminar", command=lambda: self.eliminar_tarea(self.task_id), 
                                   bg="red", activebackground="#8B0000", 
                               activeforeground="white", fg="white", font=('FontAwesome', 12, "bold"))
    self.delete_button.pack(fill="x", padx=8, pady=8, side="bottom")

  # Función para marcar como completada/no completada a la tarea, y hacer los respectivos cambios en la misma
  def completar_tarea(self, task_id, status):
    today = date.today()
    if status != 0:
      today = None
    db.db_controller.completeTask(not status, today, task_id)
    self.top.destroy()
    self.tareas_ui.update_tareas_list()
    self.tareas_ui.update_scrollbar()

  # Función para editar los datos de una tarea
  def editar_tarea(self, tarea):
    AddTareaDialog(self.top, self.tareas_ui, tarea, self.top)

  # Función para eliminar una tarea
  def eliminar_tarea(self, task_id):
    confirmacion = messagebox.askyesno("Confirmar eliminación", "¿Estás seguro de que quieres eliminar esta tarea?\nPerderas toda la información relacionada con la tarea")
    if confirmacion:
      db.db_controller.deleteTaskByID(task_id)
      self.top.destroy()
      self.tareas_ui.update_tareas_list()
      self.tareas_ui.update_scrollbar()