import tkinter as tk
from .add_tarea import AddTareaDialog
from .tareas_info_UI import TareasInfo
from DB import controller as db

class TareasUI:

  def __init__(self, root):
    self.root = root
    tk.Label(root, text="Tareas", font=('FontAwesome', 18, "bold")).pack(side="top")

    self.estado = tk.BooleanVar()
    check_button = tk.Checkbutton(root, text="Mostrar tareas completedas", variable=self.estado, command=lambda: self.toggle_completed_tasks(), font=('FontAwesome', 14))
    check_button.pack(anchor="e", padx=16)

    # Abrir la ventana para crear tareas
    def add_task():
      AddTareaDialog(root, self, None, None)

    # Botón que agrega tareas
    add_task_button = tk.Button(root, text="Añadir tarea", command=add_task, bg="#496fe8", activebackground="#2b3fca",
                              activeforeground="white", fg="white", font=('FontAwesome', 14, "bold"))
    add_task_button.pack(pady=16, padx=16, side="bottom", anchor="ne")

    # Creación del canvas que contendra la lista
    self.canvas = tk.Canvas(self.root, yscrollincrement=0)
    self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=16, pady=16)

    # Creación del scrollbar
    self.scrollbar = tk.Scrollbar(self.root, orient=tk.VERTICAL, command=self.canvas.yview)
    self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Configuración de la lista
    self.update_tareas_list()
    self.update_scrollbar()

  def toggle_tasks(self):
      if self.estado.get():
          return db.db_controller.getAllTaskWithSubjectColor() # Recuperamos todas las tareas
      else:
          return db.db_controller.getAllNotCompleteTaskWithSubjectColor() # Recuperamos solo las tareas no 

  def toggle_completed_tasks(self):
      if self.estado.get(): # Recuperamos todas las tareas
          self.update_tareas_list()
          self.update_scrollbar()
      else: # Recuperamos solo las tareas no
          self.update_tareas_list()
          self.update_scrollbar()

    # Función para crear los espacios para cada tarea
  def draw_rectangles(self):
      self.rectangles = []
      y_position = 0
      x_start = 0
      x_end = 825
      for i, (id, task, subject, color, date, type, complete) in enumerate(self.data):
        rectangle = self.canvas.create_rectangle(x_start, y_position, x_end, y_position + 55, outline="",
                                                   tags=f"rectangle{i}")
        self.rectangles.append(rectangle)
        self.canvas.create_line(x_start, y_position + 55, x_end, y_position + 55,
                                fill="light grey")  # Agregar un divisor al final del rectángulo
        if complete:
           self.canvas.create_text(10, y_position + 15, anchor='w', text=task, font=('FontAwesome', 15,"overstrike"))
        else:
           self.canvas.create_text(10, y_position + 15, anchor='w', text=task, font=('FontAwesome', 15))
        self.canvas.create_oval(10, y_position + 30, 30, y_position + 50, fill=color, outline="")  # Dibujar círculo de color dentro del rectángulo
        self.canvas.create_text(40, y_position + 40, anchor='w', text=subject, font=('FontAwesome', 15))
        self.canvas.create_text(x_end - 110, y_position + 15, anchor='w', text=date, font=('FontAwesome', 15))
        self.canvas.create_text(x_end - 165, y_position + 40, anchor='w', text=type, font=('FontAwesome', 15))

        # Eventos relacionados al comportamiento del rectangulo, como lo puede ser el pasar por encima o hacer click en el
        self.canvas.tag_bind(f"rectangle{i}", '<ButtonPress-1>', lambda event, id=id: self.on_item_click(id))
        self.canvas.tag_bind(rectangle, "<Enter>", lambda event, rect=rectangle: self.on_enter(rect))
        self.canvas.tag_bind(rectangle, "<Leave>", lambda event, rect=rectangle: self.on_leave(rect))

        y_position += 55

  # Función para actualizar el comportamiento de la scrollbar en base a cuantos elementos tiene la base de datos
  def update_scrollbar(self):
    item_count = len(self.data)
    if item_count > 10:# Si tiene mas de 10 elementos, mostramos la scrollbar con sus respectivos comportamientos
        self.scrollbar_visible = True
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<MouseWheel>", lambda e: self.canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))
    else:# Si no, ocultamos y quitamos todo comportamiento relacionado al scroll
        self.scrollbar_visible = False
        self.canvas.configure(yscrollcommand=None)
        self.canvas.unbind("<Configure>")
        self.canvas.unbind("<MouseWheel>")

    if self.scrollbar_visible:
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    else:
        self.scrollbar.pack_forget()

  # Función para actualizar la lista de tareas
  def update_tareas_list(self):
    # Actualizar la lista de tareas
    self.data = self.toggle_tasks()
    self.canvas.delete("all")  # Limpiar el Canvas
    self.draw_rectangles()

  # Función para detectar qué tarea se selecciono
  def on_item_click(self, id):
    TareasInfo(self.root, self, id)

  def on_enter(self, rect):
    # Cambiar estilo al pasar el ratón por encima
     self.canvas.itemconfig(rect, fill="#9bb8f5")

  def on_leave(self,rect):
    # Restaurar estilo al salir el ratón
    self.canvas.itemconfig(rect, fill="")