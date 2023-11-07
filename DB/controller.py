import sqlite3 as sql

class db_controller:

  #def createDB():
  #  conn = sql.connect("edutrack.db")
  #  conn.commit()
  #  conn.close()

  # Ingresar una materia a la base de datos
  def insertSubject(materia, color):
    createSubjectTable()
    conn = sql.connect("edutrack.db")
    cursor = conn.cursor()
    instruccion = f"INSERT INTO subject (materia, color) VALUES (?, ?)"
    cursor.execute(instruccion, (materia, color))
    conn.commit()
    conn.close()

  def getSubjectID(materia):
    conn = sql.connect("edutrack.db")
    cursor = conn.cursor()
    instruccion = f"SELECT id WHERE subject materia=?"
    cursor.execute(instruccion, materia)
    print(f"{cursor.fetchone()}       {cursor.fetchone()[0]}")
    return cursor.fetchone()
  
  # Ingresar una tarea a la base de datos
  def insertTask(tarea, materia_id, fecha, type):
    createTaskTable()
    conn = sql.connect("edutrack.db")
    cursor = conn.cursor()
    instruccion = f"INSERT INTO task (tarea, subject_id, fecha, type) VALUES (?, ?, ?, ?)"
    cursor.execute(instruccion, (tarea, materia_id, fecha, type))
    conn.commit()
    conn.close()
  
  # Obtener los todos los datos de materias de la base de datos
  def getAllSubject():
    conn = sql.connect("edutrack.db")
    cursor = conn.cursor()
    instruccion = f"SELECT * FROM subject ORDER BY LOWER(materia)"
    cursor.execute(instruccion)
    datos = cursor.fetchall()
    conn.commit()
    conn.close()
    return datos
  
# Creación de la tabla de Materias
def createSubjectTable():
    conn = sql.connect("edutrack.db")
    cursor = conn.cursor()
    cursor.execute(
      """CREATE TABLE IF NOT EXISTS subject (
        id INTEGER PRIMARY KEY,
        materia TEXT NOT NULL UNIQUE,
        color TEXT NOT NULL
      )"""
    )
    conn.commit()
    conn.close()

# Creación de la tabla de Tareas
def createTaskTable():
    conn = sql.connect("edutrack.db")
    cursor = conn.cursor()
    cursor.execute(
      """CREATE TABLE IF NOT EXISTS Task (
        id INTEGER PRIMARY KEY,
        tarea TEXT NOT NULL,
        materia_id INTEGER NOT NULL,
        fecha TEXT NOT NULL,
        type TEXT NOT NULL,
        FOREIGN KEY(materia_id) REFERENCES subject(id)
      )"""
    )
    conn.commit()
    conn.close()