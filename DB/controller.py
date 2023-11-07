import sqlite3 as sql

class db_controller:

  #def createDB():
  #  conn = sql.connect("edutrack.db")
  #  conn.commit()
  #  conn.close()

  def createSubjectTable():
    conn = sql.connect("edutrack.db")
    cursor = conn.cursor()
    cursor.execute(
      """CREATE TABLE IF NOT EXISTS subject (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        materia TEXT NOT NULL,
        color TEXT NOT NULL
      )"""
    )
    conn.commit()
    conn.close()

  def insertSubject(materia, color):
    conn = sql.connect("edutrack.db")
    cursor = conn.cursor()
    instruccion = f"INSERT INTO subject VALUES ('{materia}', '{color}')"
    cursor.execute(instruccion)
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