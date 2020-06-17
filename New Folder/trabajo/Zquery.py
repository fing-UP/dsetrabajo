import sqlite3
database = sqlite3.connect("linioexp_parcial_lab3.db")  # ABRIR CONEXION CON BASE DE DATOS
lista=[]

cursor = database.cursor()  # OBTENER OBJETO CURSOR
query = '''SELECT *  FROM colaborador
                '''
cursor.execute(query)
lista=cursor.fetchall()
print(lista)
