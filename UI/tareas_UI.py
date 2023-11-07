import tkinter as tk
#from .add_tarea import AddTareaDialog
from DB import controller as db

class TareasUI:

  def __init__(self, root):
    self.root = root
    tk.Label(root, text="Tareas", font=('FontAwesome', 18, "bold")).pack(side="top")

    # Abrir la ventana para crear tareas
    def add_task():
      a = 1
      #AddTareaDialog(root, self)

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

    # Datos de prueba, se remplazarán con datos reales
    self.data = [("Tarea 1", "Matemáticas", "2023-11-15"), ("Tarea 2", "Ciencias", "2023-11-20"),
                 ("Tarea 3", "Historia", "2023-11-25"), ("Tarea 4", "Ciencias", "2023-11-20"),
                 ("Tarea 5", "Matemáticas", "2023-11-15"), ("Tarea 6", "Ciencias", "2023-11-20"),
                 ("Tarea 7", "Matemáticas", "2023-11-15"), ("Tarea 8", "Ciencias", "2023-11-20"),
                 ("Tarea 9", "Matemáticas", "2023-11-15"), ("Tarea 10", "Ciencias", "2023-11-20")]

    # Configuración del scroll de la lista
    self.update_scrollbar()

    self.draw_rectangles()

    # Función para crear los espacios para cada tarea
  def draw_rectangles(self):
      self.rectangles = []
      y_position = 0
      x_start = 0
      x_end = 825
      for i, (task, subject, date) in enumerate(self.data):
        rectangle = self.canvas.create_rectangle(x_start, y_position, x_end, y_position + 55, outline="",
                                                   tags=f"rectangle{i}")
        self.rectangles.append(rectangle)
        self.canvas.create_line(x_start, y_position + 55, x_end, y_position + 55,
                                fill="light grey")  # Agregar un divisor al final del rectángulo
        self.canvas.create_text(10, y_position + 15, anchor='w', text=task, font=('FontAwesome', 15))
        self.canvas.create_oval(10, y_position + 30, 30, y_position + 50, fill="red", outline="")  # Dibujar círculo de color dentro del rectángulo
        self.canvas.create_text(40, y_position + 40, anchor='w', text=subject, font=('FontAwesome', 15))
        self.canvas.create_text(x_end - 110, y_position + 15, anchor='w', text=date, font=('FontAwesome', 15))
        self.canvas.create_text(x_end - 165, y_position + 40, anchor='w', text="Trabajo en equipo", font=('FontAwesome', 15))

        # Eventos relacionados al comportamiento del rectangulo, como lo puede ser el pasar por encima o hacer click en el
        self.canvas.tag_bind(f"rectangle{i}", '<ButtonPress-1>', lambda event, i=i: self.on_item_click(event, i))
        self.canvas.tag_bind(rectangle, "<Enter>", lambda event, rect=rectangle: self.on_enter(rect))
        self.canvas.tag_bind(rectangle, "<Leave>", lambda event, rect=rectangle: self.on_leave(rect))

        y_position += 55

  # Función para actualizar el comportamiento de la scrollbar en base a cuantos elementos tiene la base de datos
  def update_scrollbar(self):
    item_count = len(self.data)
    if item_count > 10:# Si tiene mas de 18 elementos, mostramos la scrollbar con sus respectivos comportamientos
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

  # Función para detectar qué tarea se selecciono
  def on_item_click(self, event, i):
    print(f"Seleccionaste: {self.data[i][0]}")

  def on_enter(self, rect):
    # Cambiar estilo al pasar el ratón por encima
     self.canvas.itemconfig(rect, fill="#9bb8f5")

  def on_leave(self,rect):
    # Restaurar estilo al salir el ratón
    self.canvas.itemconfig(rect, fill="")