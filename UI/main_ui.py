import tkinter as tk
from .tareas_UI import TareasUI
from .materias_UI import MateriasUI

bg_color = '#dee6fb'
hover_color = '#3552dc'

class MainUI:

  def __init__(self, root):
    self.root = root
    
    # Congfiguración de la ventana inicial
    self.root.title("EduTrack")
    self.root.geometry("1100x700")
    self.root.resizable(0, 0)

    ancho_menu = 20
    alto_menu = 2
    font_awesome = ('FontAwesome', 15)

    # Cración del menu lateral
    self.sidebar = tk.Frame(root, bg=bg_color)
    self.sidebar.pack(side=tk.LEFT, fill="both", expand=False)

    self.main = tk.Frame(root)
    self.main.pack(side=tk.RIGHT, fill='both', expand=True)

    # Botones del menú lateral
    self.buttonTask = tk.Button(self.sidebar)
    self.buttonSubject = tk.Button(self.sidebar)

    buttons_info = [
      ("Tareas", "\uf00c", self.buttonTask,self.abrir_tareas),
      ("Materias", "\uf02d", self.buttonSubject,self.abrir_materias)
      ]
    
    for text, icon, button,comando in buttons_info:
      self.configurar_boton_menu(button, text, icon, font_awesome, ancho_menu, alto_menu,comando)
    self.abrir_tareas()

  def configurar_boton_menu(self, button, text, icon, font_awesome, ancho_menu, alto_menu, comando):
    button.config(text=f"  {icon}    {text}", anchor="w", font=font_awesome,
                  bd=0, bg=bg_color, fg="black", width=ancho_menu, height=alto_menu,
                  command = comando)
    button.pack(fill="x",side=tk.TOP)
    self.bind_hover_events(button)
  
  def bind_hover_events(self, button):
    # Asociar eventos Enter y Leave con la función dinámica
    button.bind("<Enter>", lambda event: self.on_enter(event, button))
    button.bind("<Leave>", lambda event: self.on_leave(event, button))

  def on_enter(self, event, button):
    # Cambiar estilo al pasar el ratón por encima
    button.config(bg=hover_color, fg='white')

  def on_leave(self, event, button):
    # Restaurar estilo al salir el ratón
    button.config(bg=bg_color, fg='black')
  
  # Nuevo
  def abrir_tareas(self):   
    self.limpiar_panel(self.main)
    TareasUI(self.main)
        
  def abrir_materias(self):   
    self.limpiar_panel(self.main)
    MateriasUI(self.main)

  def limpiar_panel(self,panel):
    # Función para limpiar el contenido del panel
    for widget in panel.winfo_children():
      widget.destroy()