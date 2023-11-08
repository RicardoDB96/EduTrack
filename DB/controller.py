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
    id = cursor.fetchone()
    conn.commit()
    conn.close()
    return id
  
  # Ingresar una tarea a la base de datos
  def insertTask(tarea, materia_id, fecha, type):
    createTaskTable()
    conn = sql.connect("edutrack.db")
    cursor = conn.cursor()
    instruccion = "INSERT INTO task (tarea, subject_id, fecha, type) VALUES (?, ?, ?, ?)"
    cursor.execute(instruccion, (tarea, materia_id, fecha, type))
    conn.commit()
    conn.close()

  # Actualizar una tarea a la base de datos
  def updateTask(tarea, materia_id, fecha, type, task_id):
    conn = sql.connect("edutrack.db")
    cursor = conn.cursor()
    instruccion = """UPDATE task 
                    SET tarea = ?, 
                        subject_id = ?, 
                        fecha = ?, 
                        type = ?
                    WHERE id = ?"""
    cursor.execute(instruccion, (tarea, materia_id, fecha, type, task_id))
    conn.commit() 
    conn.close()

  # Actualizar una materia a la base de datos
  def updateSubject(id, materia, color):
    conn = sql.connect("edutrack.db")
    cursor = conn.cursor()
    instruccion = """UPDATE subject 
                    SET materia = ?, 
                        color = ?
                    WHERE id = ?"""
    cursor.execute(instruccion, (materia, color, id))
    conn.commit() 
    conn.close()

  # Obtener los todos los datos de la tarea, según su ID, de la base de datos con los datos de la materia a la que pertenece
  def getTaskByID(id):
    conn = sql.connect("edutrack.db")
    cursor = conn.cursor()
    instruccion = f"""
      SELECT task.tarea, subject.materia, subject.color, task.fecha, task.type, task.complete, task.completed, task.id
      FROM task 
      JOIN subject 
      ON task.subject_id = subject.id
      WHERE task.id = {id}
    """
    cursor.execute(instruccion)
    tarea = cursor.fetchone()
    conn.commit()
    conn.close()
    return tarea
  
  # Obtener los todos los datos de la materia, según su ID
  def getSubjectByID(id):
    conn = sql.connect("edutrack.db")
    cursor = conn.cursor()
    instruccion = f"""
      SELECT id, materia, color
      FROM subject
      WHERE id = {id}
    """
    cursor.execute(instruccion)
    materia = cursor.fetchone()
    conn.commit()
    conn.close()
    return materia
  
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
  
  # Función para cambiar el estado de completo de una tarea
  def completeTask(complete, completed, task_id):
    conn = sql.connect("edutrack.db")
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE task
    SET complete = ?,
        completed = ?
    WHERE id = ?""", (complete, completed, task_id))
    conn.commit()
    conn.close()
  
  # Función para contar el numero de tareas que pertenecen a una materia
  def getTaskCountFromSubjectByID(subject_id):
    conn = sql.connect('edutrack.db')  # Reemplaza 'example.db' con el nombre de tu base de datos
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM Task WHERE subject_id=?", (subject_id,))
    task_count = cursor.fetchone()[0]
    conn.close()
    return task_count
  
  # Función para contar el numero de tareas completadas que pertenecen a una materia
  def getCompleteTaskCountFromSubjectByID(subject_id):
    conn = sql.connect('edutrack.db')  # Reemplaza 'example.db' con el nombre de tu base de datos
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM Task WHERE subject_id=? AND complete=1", (subject_id,))
    complete_task_count = cursor.fetchone()[0]
    conn.close()
    return complete_task_count
  
  def deleteTaskByID(id):
    conn = sql.connect('edutrack.db')
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM Task WHERE id={id}")
    conn.commit()
    conn.close()

  def deleteSubjectByID(subject_id):
    conn = sql.connect('edutrack.db')  # Reemplaza 'example.db' con el nombre de tu base de datos
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Task WHERE subject_id=?", (subject_id,))
    cursor.execute("DELETE FROM Subject WHERE id=?", (subject_id,))
    conn.commit()
    conn.close()
  
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
      complete INTEGER DEFAULT 0,
      completed TEXT DEFAULT NULL,
      description TEXT DEFAULT NULL,
      FOREIGN KEY(subject_id) REFERENCES subject(id)
    )"""
  )
  conn.commit()
  conn.close()