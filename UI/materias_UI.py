import tkinter as tk

class MateriasUI:

  def __init__(self, root):
    self.root = root
    tk.Label(root, text="Materias", font=('FontAwesome', 18, "bold")).pack(side="top")

    # Botón que agrega materias
    add_subject_button = tk.Button(root, text="Añadir materia", bg="#496fe8", activebackground="#2b3fca", activeforeground="white", fg="white", font=('FontAwesome', 14, "bold"))
    add_subject_button.pack(pady=16, padx=16,side="bottom", anchor="ne")

    # Creación del canvas que contendra la lista
    self.canvas = tk.Canvas(self.root, yscrollincrement=0)
    self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=16, pady=16)

    # Creación del scrollbar
    self.scrollbar = tk.Scrollbar(self.root, orient=tk.VERTICAL, command=self.canvas.yview)
    self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Configuración del scroll de la lista
    self.canvas.configure(yscrollcommand=self.scrollbar.set)
    self.canvas.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
    self.canvas.bind("<MouseWheel>",lambda e: self.canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
    
    # Datos de prueba, se remplazaran
    self.data = [("Matemáticas", "red"), ("Ciencias", "green"), ("Historia", "blue"),("Matemáticas", "red"), ("Ciencias", "green"), ("Historia", "blue"),("Matemáticas", "red"), ("Ciencias", "green"), ("Historia", "blue"),("Matemáticas", "red"), ("Ciencias", "green"), ("Historia", "blue"), ("Matemáticas", "red"), ("Ciencias", "green"), ("Historia", "blue"),("Matemáticas", "red"), ("Ciencias", "green"), ("Historia", "blue"),("Matemáticas", "red"), ("Ciencias", "green"), ("Historia", "blue"),("Matemáticas", "red"), ("Ciencias", "green"), ("Historia", "black"),]

    self.draw_rectangles()
    
  # Función para crear los espacios para cada materias¿
  def draw_rectangles(self):
    self.rectangles = []
    y_position = 0
    x_start = 0
    x_end = 825
    for i, (subject, color) in enumerate(self.data):
      rectangle = self.canvas.create_rectangle(x_start, y_position, x_end, y_position + 30, outline="", tags=f"rectangle{i}")
      self.rectangles.append(rectangle)
      self.canvas.create_line(x_start, y_position + 30, x_end, y_position + 30, fill="light grey")  # Agregar un divisor al final del rectángulo
      circle = self.canvas.create_oval(10, y_position + 5, 30, y_position + 25, fill=color, outline="")  # Dibujar círculo de color dentro del rectángulo
      self.canvas.create_text(40, y_position + 15, anchor='w', text=subject, font=('FontAwesome', 15))  # Agregar texto con el nombre de la materia al lado del círculo
      self.canvas.tag_bind(f"rectangle{i}", '<ButtonPress-1>', lambda event, i=i: self.on_item_click(event, i))
      self.canvas.tag_bind(rectangle, "<Enter>", lambda event, rect=rectangle: self.on_enter(rect))
      self.canvas.tag_bind(rectangle, "<Leave>", lambda event, rect=rectangle: self.on_leave(rect))
      y_position += 30

  # 
  def on_item_click(self, event, i):
      print(f"Seleccionaste: {self.data[i][0]}")

  def on_enter(self, rect):
    # Cambiar estilo al pasar el ratón por encima
     self.canvas.itemconfig(rect, fill="#9bb8f5")

  def on_leave(self,rect):
    # Restaurar estilo al salir el ratón
    index = self.rectangles.index(rect)
    color = self.data[index][1]
    self.canvas.itemconfig(rect, fill="")