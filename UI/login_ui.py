import tkinter as tk

class LoginUI:
  
  def __init__(self, root):
    self.root = root
    self.root.title("Login")
    self.root.geometry("300x200")
    self.username_label = tk.Label(root, text="Username")
    self.username_label.pack()
    self.username_entry = tk.Entry(root)
    self.username_entry.pack()
    self.password_label = tk.Label(root, text="Password")
    self.password_label.pack()
    self.password_entry = tk.Entry(root, show="*")
    self.password_entry.pack()
    self.login_button = tk.Button(root, text="Login")
    self.login_button.pack()