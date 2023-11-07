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
  
# Creación de la tabla
def createSubjectTable():
    conn = sql.connect("edutrack.db")
    cursor = conn.cursor()
    cursor.execute(
      """CREATE TABLE IF NOT EXISTS subject (
        id INTEGER PRIMARY KEY,
        materia TEXT NOT NULL,
        color TEXT NOT NULL
      )"""
    )
    conn.commit()
    conn.close()