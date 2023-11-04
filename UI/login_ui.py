import tkinter as tk

class LoginUI:

  # Mostrar/Ocular contraseña logica
  def toggle_password(self):
    if self.password_state.get():
      self.password_entry.config(show='')
    else:
      self.password_entry.config(show='*')
  
  def __init__(self, root):
    self.root = root
    
    # Congfiguración de la ventana inicial
    self.root.title("Login")
    self.root.geometry("300x200")
    self.root.resizable(0, 0)

    # Fuentes a utilizar
    n_font = ("Fira Code", 12)
    b_font = ("Fira Code bold", 12)

    # Nombre del sistema
    tk.Label(root, text="EduTrack", font=("Fira Code bold", 18), fg="#2935a4").pack(side="top", fill="x", padx=8, pady=12)

    # Acomodo del Username
    username_frame = tk.Frame(root)
    username_frame.pack(fill="x")
    tk.Label(username_frame, text="Usuario   ", font=b_font).pack(side="left", padx=8, expand=False)
    username_entry = tk.Entry(username_frame, font=n_font)
    username_entry.pack(side="right", fill="x", padx=8, expand=True)

    # Acomodo del Password
    password_frame = tk.Frame(root)
    password_frame.pack()
    tk.Label(password_frame, text="Contraseña", font=b_font).pack(side="left", padx=8, expand=False)
    self.password_entry = tk.Entry(password_frame, show="*", font=n_font)
    self.password_entry.pack(side="right", fill="x", padx=8, expand=True)

    self.password_state = tk.BooleanVar()

    # Mostar/Ocultar Password
    tk.Checkbutton(root, text="Mostrar contraseña", variable=self.password_state, command=self.toggle_password, font=n_font).pack()

    # Creación del botón de Login
    login_button = tk.Button(root, text="Iniciar sesión", bg="#496fe8", activebackground="#2b3fca", activeforeground="white", fg="white", font=b_font)
    login_button.pack(fill="x", pady=16, padx=16, side="bottom")