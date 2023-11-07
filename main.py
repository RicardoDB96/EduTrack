from UI.gui_manager import GUIManager as GUI
import DB.controller as db

def main():
    # Iniciar la interfaz
    gui = GUI()
    gui.run()

    # Crear las tablas necesarias en la Base de Datos
    db.createSubjectTable()
    db.createTaskTable()

if __name__ == "__main__":
    main()