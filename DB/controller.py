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

  # Función para obtener el ID de una materia solo con su nombre
  def getSubjectID(materia):
    conn = sql.connect("edutrack.db")
    cursor = conn.cursor()
    instruccion = f"SELECT id FROM subject WHERE materia=?"
    cursor.execute(instruccion, (materia,))
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
  
  # Obtener los todos los datos de tareas de la base de datos con los datos de la materia
  def getAllTaskWithSubjectColor():
    conn = sql.connect("edutrack.db")
    cursor = conn.cursor()
    instruccion = f"""
      SELECT task.id, task.tarea, subject.materia, subject.color, task.fecha, task.type 
      FROM task 
      JOIN subject 
      ON task.subject_id = subject.id
      ORDER BY task.fecha
    """
    cursor.execute(instruccion)
    datos = cursor.fetchall()
    conn.commit()
    conn.close()
    return datos
  
  # Obtener los todos los nombres de materias de la base de datos
  def getAllSubjectNames():
    conn = sql.connect("edutrack.db")
    cursor = conn.cursor()
    instruccion = f"SELECT materia FROM subject ORDER BY LOWER(materia)"
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
    """CREATE TABLE IF NOT EXISTS task (
      id INTEGER PRIMARY KEY,
      tarea TEXT NOT NULL,
      subject_id INTEGER NOT NULL,
      fecha TEXT NOT NULL,
      type TEXT NOT NULL,
      FOREIGN KEY(subject_id) REFERENCES subject(id)
    )"""
  )
  conn.commit()
  conn.close()