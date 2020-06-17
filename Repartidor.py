from Persona import Persona
from datetime import datetime
import sqlite3
class Repartidor(Persona):
    def __init__(self, nombre:str=None,apellidoPaterno:str=None,apellidoMaterno:str=None,dni:str=None,fechaNacimiento:datetime=None,fechaIngreso:datetime=None, idRepartidor:str=None,genero:bool=None):
        self.__idRepartidor=idRepartidor if idRepartidor is not None else self.generarIdRepartidor()
        self.__fechaIngreso=fechaIngreso
        self.__listaOrden=self.generarListaOrden()
        Persona.__init__(self, nombre, apellidoPaterno, apellidoMaterno, dni, fechaNacimiento,genero)

    @property
    def idRepartidor(self):
        return self.__idRepartidor
    @idRepartidor.setter
    def idRepartidor(self,newidRepartidor):
        self.__idRepartidor=newidRepartidor
    @property
    def fechaIngreso(self):
        return self.__fechaIngreso
    @fechaIngreso.setter
    def fechaIngreso(self,newfechaIngreso):
        self.__fechaIngreso=newfechaIngreso

    def generarIdRepartidor(self):
        count = 0
        database = sqlite3.connect("linioexp_parcial_lab3.db")  # ABRIR CONEXION CON BASE DE DATOS
        try:
            cursor = database.cursor()  # OBTENER OBJETO CURSOR
            query = '''
            SELECT COUNT(*) FROM repartidor'''
            cursor.execute(query)
            count = cursor.fetchone()
        except Exception as e:
            print("Error: {}".format(e))
        finally:
            database.close()  # CERRAR CONEXION CON BASE DE DATOS

        return "REP" + "0"*(4 - len(str(count[0] + 1))) + str(count[0] + 1)
    def eliminarRepartidor(self):
        database = sqlite3.connect("linioexp_parcial_lab3.db")  # ABRIR CONEXION CON BASE DE DATOS

        try:
            cursor = database.cursor()  # OBTENER OBJETO CURSOR
            query = '''
                            DELETE FROM repartidor where idRepartidor= '{}'
                            '''.format(self.__idRepartidor)
            cursor.execute(query)
                

            database.commit()
        except Exception as e:
            print("Error: {}".format(e))
        finally:
            database.close()
    def actualizarRepartidor(self):
        database = sqlite3.connect("linioexp_parcial_lab3.db")
        try:

            cursor = database.cursor()
            query = '''                 
            UPDATE repartidor
            SET dni = '{}', nombre = '{}', apellidoPaterno = '{}', apellidoMaterno = '{}',
            genero = '{}', fechaNacimiento = {}, fechaIngreso = '{}'        
            WHERE idRepartidor = '{}'
            '''.format(self.dni, self.nombre, self.apellidoPaterno,
                        self.apellidoMaterno, self.genero, self.fechaNacimiento,
                         self.__fechaIngreso,self.__idRepartidor)
            cursor.execute(query)
            database.commit()
            estado_op = True
        except Exception as e:
            database.rollback()  # RESTAURAR ANTES DE CAMBIOS POR ERROR
            print("Error: {}".format(e))
        finally:
            database.close() 
    def agregarRepartidor(self):
        database = sqlite3.connect("linioexp_parcial_lab3.db")  # ABRIR CONEXION CON BASE DE DATOS
        try:

            cursor = database.cursor()  # OBTENER OBJETO CURSOR
            query = '''
            INSERT INTO repartidor(idRepartidor,dni, nombre, apellidoPaterno, apellidoMaterno, genero, fechaIngreso, fechaNacimiento)
            VALUES ('{}', '{}', '{}', '{}','{}', '{}', '{}','{}')'''.format(self.__idRepartidor,self.dni,
                       self.nombre, self.apellidoPaterno,
                       self.apellidoMaterno, self.genero, self.__fechaIngreso, self.fechaNacimiento)
            cursor.execute(query)
            database.commit()  # CONFIRMAR CAMBIOS QUERY
            estado_op = True
        except Exception as e:
            database.rollback()  # RESTAURAR ANTES DE CAMBIOS POR ERROR
            print("Error: {}".format(e))
        finally:
            database.close() 
    def obtenerRepartidor(self):
        database = sqlite3.connect("linioexp_parcial_lab3.db")

        try:
            cursor = database.cursor()
            query = '''
                    SELECT * from repartidor 
                    WHERE idCliente = '{}' 
                    '''.format(self.__idRepartidor)
            cursor.execute(query)
            lista = cursor.fetchall()[0]
            self.nombre=lista[1]
            self.apellidoPaterno=lista[2]
            self.apellidoMaterno=lista[3]
            self.dni=lista[4]
            self.fechaNacimiento=lista[6]
            self.__fechaIngreso=lista[5]
            
           
        except Exception as e:
            print("Error: {}".format(e))
        finally:
            database.close() 
    def generarListaOrden(self):
        database = sqlite3.connect("linioexp_parcial_lab3.db")  # ABRIR CONEXION CON BASE DE DATOS
        lista=[]
        try:
            cursor = database.cursor()  # OBTENER OBJETO CURSOR

            query = '''SELECT *  FROM orden where idRepartidor= '{}'
                '''.format(self.__idRepartidor)
            cursor.execute(query)
            cursor.fetchall()

            database.commit()
        except Exception as e:
            print("Error: {}".format(e))
        finally:
            database.close()
        return lista
