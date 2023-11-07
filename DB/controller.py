import sqlite3 as sql

class db_controller:

  #def createDB():
  #  conn = sql.connect("edutrack.db")
  #  conn.commit()
  #  conn.close()

  def insertSubject(materia, color):
    createSubjectTable()
    conn = sql.connect("edutrack.db")
    cursor = conn.cursor()
    instruccion = f"INSERT INTO subject (materia, color) VALUES (?, ?)"
    cursor.execute(instruccion, (materia, color))
    conn.commit()
    conn.close()
  
  def getAllSubject():
    conn = sql.connect("edutrack.db")
    cursor = conn.cursor()
    instruccion = f"SELECT * FROM subject"
    cursor.execute(instruccion)
    datos = cursor.fetchall()
    conn.commit()
    conn.close()
    return datos
  
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