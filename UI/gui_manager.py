import tkinter as tk
from .login_ui import LoginUI
from .main_ui import MainUI

class GUIManager:
  def __init__(self):
    self.root = tk.Tk()
    self.root.iconbitmap('EduTrack.ico')
    #self.login_ui = LoginUI(self.root)
    self.main_ui = MainUI(self.root)

  def run(self):
    self.root.mainloop()

  # Mostrar la pantalla de Login
  def show_login(self):
    self.login_ui.show()

  def hide_login(self):
    self.login_ui.hide()