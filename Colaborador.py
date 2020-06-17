import sqlite3
import datetime
from Usuario import Usuario
from Comercio import Comercio
class Colaborador(Usuario):
    def __init__(self,comercio:Comercio=None ,nombre:str=None,apellidoPaterno:str=None,apellidoMaterno:str=None,dni:str=None,fechaNacimiento:datetime=None, correo: str = None, nombreusuario: str = None, password: str = None, fechaRegistro: datetime = None, idColaborador:str=None,genero:bool=None):
        self.__idColaborador=idColaborador if idColaborador is not None else self.generarIdcolaborador()
        self.oComercio=comercio #Cambie listComercio por ocomercio
        #self.__oUsuario=Usuario()
        Usuario.__init__(self,nombre,apellidoPaterno,apellidoMaterno,dni,fechaNacimiento,correo,nombreusuario,password,fechaRegistro,genero)
    @property
    def idColaborador(self):
        return self.__idColaborador
    @idColaborador.setter
    def idColaborador(self,newidColaborador):
        self.__idColaborador=newidColaborador

    @property
    def comercio(self):
        return self.oComercio

    @comercio.setter
    def comercio(self, newComercio):
        self.oComercio = newComercio

        
    def generarIdcolaborador(self):
        count = 0
        database = sqlite3.connect("linioexp_parcial_lab3.db")  # ABRIR CONEXION CON BASE DE DATOS
        try:
            cursor = database.cursor()  # OBTENER OBJETO CURSOR
            query = '''
            SELECT COUNT(*) FROM colaborador'''
            cursor.execute(query)
            count = int(cursor.fetchone()[0])
        except Exception as e:
            print("Error: {}".format(e))
        finally:
            database.close()  # CERRAR CONEXION CON BASE DE DATOS

        return str("CO" + "0"*(4 - len(str(int(count) + 1))) + str(count + 1))
    def eliminarcolaborador(self):
        database = sqlite3.connect("linioexp_parcial_lab3.db")  # ABRIR CONEXION CON BASE DE DATOS

        try:
            cursor = database.cursor()  # OBTENER OBJETO CURSOR
            query = '''
                            DELETE * FROM colaborador where idColaborador= '{}'
                            '''.format(self.__idColaborador)
            cursor.execute(query)
            
        except Exception as e:
            print("Error: {}".format(e))
        finally:
            database.close()  # CERRAR CONEXION CON BASE DE DATOS
    def actualizarcolaborador(self): #Ya que sus atributos estan usaurio, debe ir este método?
        database = sqlite3.connect("linioexp_parcial_lab3.db")  # ABRIR CONEXION CON BASE DE DATOS

        try:
            cursor = database.cursor()  # OBTENER OBJETO CURSOR
            query = '''
            UPDATE colaborador set idComercio='{}',nombre = '{}',  apellidoMaterno= '{}',  apellidoPaterno ='{}',dni = '{}',correo = '{}',fechaNacimiento = '{}',nombreUsuario ='{}',fechaRegistro='{}',password='{}',genero='{}' where idColaborador='{}'
            '''.format(self.oComercio.idComercio,self.nombre,self.apellidoMaterno,self.apellidoPaterno,self.dni,self.correo, self.fechaNacimiento,self.nombreUsuario,self.fechaRegistro,self.password,self.genero,self.idColaborador)
            print(query)
            cursor.execute(query)
            database.commit()

        except Exception as e:
            print("Error: {}".format(e))
        finally:
            database.close()  # CERRAR CONEXION CON BASE DE DATOS
            
    def agregarcolaborador(self):
        database = sqlite3.connect("linioexp_parcial_lab3.db")  # ABRIR CONEXION CON BASE DE DATOS

        try:
            cursor = database.cursor()  # OBTENER OBJETO CURSOR
            query = '''
            INSERT INTO colaborador(idColaborador,idComercio,nombreUsuario,password,fechaRegistro, nombre,  apellidoMaterno,  apellidoPaterno,dni,correo,fechaNacimiento ,genero) VALUES('{}', '{}', '{}', '{}','{}', '{}', '{}','{}', '{}','{}','{}','{}') 
            
                                                '''.format(self.__idColaborador,self.oComercio.idComercio,self.nombreUsuario,self.password,datetime.datetime.now() ,self.nombre,self.apellidoMaterno,self.apellidoPaterno,self.dni,self.correo, self.fechaNacimiento, self.genero)
         
            cursor.execute(query)
            database.commit()
        except Exception as e:
            print("Error: {}".format(e))
        finally:
            database.close()  # CERRAR CONEXION CON BASE DE DATOS
    def obtenercolaborador(self):
        database = sqlite3.connect("linioexp_parcial_lab3.db")

        try:
            cursor = database.cursor()
            query = '''
                    SELECT * from colaborador 
                    WHERE idColaborador = '{}' 
                    '''.format(self.__idColaborador)
            cursor.execute(query)

            lista = cursor.fetchall()[0]

            self.oComercio=Comercio(idComercio=lista[1])
            self.oComercio.obtenerComercio()
            self.nombreUsuario=lista[2]
            self.password=lista[3]
            self.fechaRegistro=lista[4]
            self.nombre=lista[5]
            self.apellidoMaterno=lista[6]
            self.apellidoPaterno=lista[7]
            self.dni=lista[8]
            self.correo=lista[9]
            self.fechaNacimiento=lista[10]
            self.genero=lista[11]
            
           
        except Exception as e:
            print("Error: {}".format(e))
        finally:
            database.close() 
    def iniciarSesion(self):
        database = sqlite3.connect("linioexp_parcial_lab3.db")  # ABRIR CONEXION CON BASE DE DATOS
        texto = 0
        try:
            cursor = database.cursor()  # OBTENER OBJETO CURSOR

            query = '''SELECT *  FROM colaborador where (nombreusuario= '{}'or correo='{}') and password='{}'
                '''.format(self.nombreUsuario, self.correo, self.password)
            cursor.execute(query)
            lista = cursor.fetchall()
            if (len(lista) == 0):
                texto = 0
            else:
                texto = 1
                self.idColaborador = lista[0][0]
                self.obtenercolaborador()

            database.commit()
        except Exception as e:
            print("Error: {}".format(e))
        finally:
            database.close()
        return texto
    def verificarUnique(self,variable):
        database = sqlite3.connect("linioexp_parcial_lab3.db")  # ABRIR CONEXION CON BASE DE DATOS
        texto = 1
        try:
            cursor = database.cursor()  # OBTENER OBJETO CURSOR

            query = '''SELECT *  FROM colaborador where nombreusuario= '{}'or correo='{}' 
                '''.format(variable,variable)
            cursor.execute(query)
            lista = cursor.fetchall()
            if (len(lista) == 0):
                texto = 1
            else:
                texto = 0


            database.commit()
        except Exception as e:
            print("Error: {}".format(e))
        finally:
            database.close()
        return texto