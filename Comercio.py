
import sqlite3

#En revision
class Comercio(object):

    def __init__(self, idComercio: str = None,ruc:str=None,nombre:str=None):
        self.__idComercio=idComercio if idComercio is not None else self.generarIdComercio()
        self.__ruc=ruc
        self.__nombre=nombre
        #self.oLocalizacion=localizacion
        
    #Atributos
    @property
    def idComercio(self):
        return self.__idComercio
    @idComercio.setter
    def idComercio(self, newidComercio):
        self.__idComercio = newidComercio
    @property
    def ruc(self):
        return self.__ruc
    @ruc.setter
    def ruc(self, newruc):
        self.__ruc = newruc
    @property
    def nombre(self):
        return self.__nombre
    @nombre.setter
    def nombre(self, newnombre):
        self.__nombre = newnombre
    @property
    def __str__(self):
        return self.__nombre
        
    #Metodos Estandares
    def generarIdComercio(self):
        count = 0
        database = sqlite3.connect("linioexp_parcial_lab3.db")  # ABRIR CONEXION CON BASE DE DATOS
        try:
            cursor = database.cursor()  # OBTENER OBJETO CURSOR
            query = '''
            SELECT COUNT(*) FROM comercio'''
            cursor.execute(query)
            count = int(cursor.fetchone()[0])
        except Exception as e:
            print("Error: {}".format(e))
        finally:
            database.close()  # CERRAR CONEXION CON BASE DE DATOS

        return "COM" + "0" * (4 - len(str(count + 1))) + str(count + 1)
    def agregarComercio(self):
        
        try:
            database = sqlite3.connect("linioexp_parcial_lab3.db")
            cursor = database.cursor() #cambiar ER: colaborador y comercio
            query = '''
                    INSERT INTO comercio(idComercio, ruc, nombre) VALUES('{}', '{}', '{}')
                    '''.format(self.__idComercio, self.__ruc, self.__nombre)
            cursor.execute(query)
            database.commit()
            
        except Exception as e:
            print("Error: {}".format(e))
        finally:
            database.close()  
    def actualizarComercio(self):
        database = sqlite3.connect("linioexp_parcial_lab3.db")  # ABRIR CONEXION CON BASE DE DATOS

        try:
            cursor = database.cursor()  # OBTENER OBJETO CURSOR
            query = '''
                        UPDATE comercio set idComercio={} ,ruc="{}", nombre="{}"
                        WHERE idComercio = '{}'
                        '''.format(self.__idComercio, self.__ruc, self.__nombre,self.__idComercio)
            cursor.execute(query)
            database.commit()
        except Exception as e:
            print("Error: {}".format(e))
        finally:
            database.close() 
    def eliminarComercio(self):
        database = sqlite3.connect("linioexp_parcial_lab3.db")  # ABRIR CONEXION CON BASE DE DATOS

        try:
            cursor = database.cursor()  # OBTENER OBJETO CURSOR
            query = '''
                            DELETE * FROM comercio where idComercio= '{}'
                            '''.format(self.__idComercio)
            cursor.execute(query)
            
        except Exception as e:
            print("Error: {}".format(e))
        finally:
            database.close()  # CERRAR CONEXION CON BASE DE DATOS
    def obtenerComercio(self):
        database = sqlite3.connect("linioexp_parcial_lab3.db")
        try:
            cursor = database.cursor()
            query = '''
                    SELECT * from comercio
                    WHERE idComercio = '{}' 
                    '''.format(self.__idComercio)
            cursor.execute(query)
            lista = cursor.fetchall()[0]
            self.__ruc=lista[1]
            self.__nombre=lista[2]
        except Exception as e:
            print("Error: {}".format(e))
        finally:
            database.close() 
    def generarListaProductos(self):
        database = sqlite3.connect("linioexp_parcial_lab3.db")  # ABRIR CONEXION CON BASE DE DATOS
        lista=[]
        try:
            cursor = database.cursor()  # OBTENER OBJETO CURSOR

            query = '''SELECT *  FROM Producto where idComercio= '{}'
                '''.format(self.__idComercio)
            cursor.execute(query)
            lista=cursor.fetchall()

            database.commit()
        except Exception as e:
            print("Error: {}".format(e))
        finally:
            database.close()
        return lista
    def generarListaColaboradores(self):
        database = sqlite3.connect("linioexp_parcial_lab3.db")  # ABRIR CONEXION CON BASE DE DATOS
        lista=[]
        try:
            cursor = database.cursor()  # OBTENER OBJETO CURSOR

            query = '''SELECT *  FROM colaborador where idComercio= '{}'
                '''.format(self.__idComercio)
            cursor.execute(query)
            lista=cursor.fetchall()

            database.commit()
        except Exception as e:
            print("Error: {}".format(e))
        finally:
            database.close()
        return lista