from Usuario import Usuario
from datetime import datetime

import sqlite3

#completamente funcional
class Cliente(Usuario):

    LISTA_ESTADO = {"NUEVO":"N", "PENDIENTE": "P", "VALIDADO": "V"}

    def __init__(self,nombre:str=None,apellidoPaterno:str=None,apellidoMaterno:str=None,dni:str=None,fechaNacimiento:datetime=None, correo: str = None, nombreusuario: str = None, password: str = None, fechaRegistro: datetime = None, idCliente:str=None, telefono: str=None , genero: bool=None):
        self.__idCliente= idCliente if idCliente is not None else self.generarIdCliente()
        self.__telefono=telefono
        self.__listaTarjetas=self.generarListaTarjeta()
        self.__listaOrden=self.generarListaOrden()
        self.__listaLocalizacion=self.generarListaLocalizacion()
        self.__lidtsCarrito=self.generarListaCarrito()
        Usuario.__init__(self,nombre,apellidoPaterno,apellidoMaterno,dni,fechaNacimiento,correo,nombreusuario,password,fechaRegistro,genero)
    def __str__(self):
        return self.idCliente + ": " + self.nombre

    @property
    def idCliente(self):
        return self.__idCliente
    @idCliente.setter
    def idCliente(self, newidCliente):
        self.__idCliente = newidCliente
    @property
    def telefono(self):
        return self.__telefono
    @telefono.setter
    def telefono(self, newtelefono):
        self.__telefono = newtelefono

    def generarIdCliente(self):
        count = 0
        database = sqlite3.connect("linioexp_parcial_lab3.db")  # ABRIR CONEXION CON BASE DE DATOS
        try:
            cursor = database.cursor()  # OBTENER OBJETO CURSOR
            query = '''
            SELECT COUNT(*) FROM cliente'''
            cursor.execute(query)
            count = int(cursor.fetchone()[0])
        except Exception as e:
            print("Error: {}".format(e))
        finally:
            database.close()  # CERRAR CONEXION CON BASE DE DATOS

        return "CLI"+"0"*(4 - len(str(count + 1))) + str(count + 1)
        #return "CLI" + "0"*(4 - len(str(count[0] + 1))) + str(count[0] + 1)
    def agregarCliente(self ):
        estado_op = False
        database = sqlite3.connect("linioexp_parcial_lab3.db")  # ABRIR CONEXION CON BASE DE DATOS
        try:

            cursor = database.cursor()  # OBTENER OBJETO CURSOR
            query = '''
            INSERT INTO cliente(idCliente,dni, nombre, apellidoPaterno, apellidoMaterno, genero, fechaRegistro, fechaNacimiento, correo, password,telefono,nombreUsuario)
            VALUES ('{}', '{}', '{}', '{}','{}', '{}', '{}', '{}','{}','{}','{}','{}')'''.format(self.__idCliente,self.dni,
                       self.nombre, self.apellidoPaterno,
                       self.apellidoMaterno, self.genero, datetime.now(), self.fechaNacimiento,
                        self.correo, self.password,self.telefono,self.nombreUsuario)
            cursor.execute(query)
            database.commit()  # CONFIRMAR CAMBIOS QUERY
            estado_op = True
        except Exception as e:
            database.rollback()  # RESTAURAR ANTES DE CAMBIOS POR ERROR
            print("Error: {}".format(e))
        finally:
            database.close()  # CERRAR CONEXION CON BASE DE DATOS

        

    def actualizarCliente(self):
        database = sqlite3.connect("linioexp_parcial_lab3.db")
        try:

            cursor = database.cursor()
            query = '''                 
            UPDATE cliente 
            SET dni = '{}', nombre = '{}', apellidoPaterno = '{}', apellidoMaterno = '{}',
            genero = '{}', fechaNacimiento = '{}', password = '{}', fechaRegistro = '{}',telefono='{}',correo='{}',nombreUsuario ='{}'        
            WHERE idCliente = '{}'
            '''.format(self.dni, self.nombre, self.apellidoPaterno,
                        self.apellidoMaterno, self.genero, self.fechaNacimiento,
                         self.password, self.fechaRegistro,self.__telefono,self.correo,self.nombreUsuario,self.__idCliente)
            cursor.execute(query)
            database.commit()
            print(query)
            estado_op = True
        except Exception as e:
            database.rollback()  # RESTAURAR ANTES DE CAMBIOS POR ERROR
            print("Error: {}".format(e))
        finally:
            database.close()  # CERRAR CONEXION CON BASE DE DATOS


    def eliminarCliente(self):
        database = sqlite3.connect("linioexp_parcial_lab3.db")  # ABRIR CONEXION CON BASE DE DATOS

        try:
            cursor = database.cursor()  # OBTENER OBJETO CURSOR
            query = '''
                            DELETE FROM cliente where idCliente= '{}'
                            '''.format(self.__idCliente)
            cursor.execute(query)
                

            database.commit()
        except Exception as e:
            print("Error: {}".format(e))
        finally:
            database.close()
    def obtenerCliente(self):
        database = sqlite3.connect("linioexp_parcial_lab3.db")

        try:
            cursor = database.cursor()
            query = '''
                    SELECT * from cliente 
                    WHERE idCliente = '{}' 
                    '''.format(self.__idCliente)
            cursor.execute(query)
            lista = cursor.fetchall()[0]
            self.nombre=lista[1]
            self.apellidoPaterno=lista[2]
            self.apellidoMaterno=lista[3]
            self.dni=lista[4]
            self.fechaNacimiento=lista[5]
            self.correo=lista[6]
            self.nombreUsuario=lista[7]
            self.password=lista[8]
            self.fechaRegistro=lista[9]
            self.telefono=lista[10]
            self.genero=lista[11]
            
           
        except Exception as e:
            print("Error: {}".format(e))
        finally:
            database.close() 
    
    
   
    def generarListaTarjeta(self):
        database = sqlite3.connect("linioexp_parcial_lab3.db")  # ABRIR CONEXION CON BASE DE DATOS
        lista=[]
        try:
            cursor = database.cursor()  # OBTENER OBJETO CURSOR

            query = '''SELECT *  FROM Tarjeta where idCliente= '{}'
                '''.format(self.__idCliente)
            cursor.execute(query)
            lista=cursor.fetchall()

            database.commit()
        except Exception as e:
            print("Error: {}".format(e))
        finally:
            database.close()
        return lista
    def generarListaOrden(self):
        database = sqlite3.connect("linioexp_parcial_lab3.db")  # ABRIR CONEXION CON BASE DE DATOS
        lista=[]
        try:
            cursor = database.cursor()  # OBTENER OBJETO CURSOR

            query = '''SELECT *  FROM orden where idCliente= '{}'
                '''.format(self.__idCliente)
            cursor.execute(query)
            lista=cursor.fetchall()

            database.commit()
        except Exception as e:
            print("Error: {}".format(e))
        finally:
            database.close()
        return lista
            
    def generarListaLocalizacion(self):
        database = sqlite3.connect("linioexp_parcial_lab3.db")  # ABRIR CONEXION CON BASE DE DATOS
        lista=[]
        try:
            cursor = database.cursor()  # OBTENER OBJETO CURSOR

            query = '''SELECT *  FROM localizacionCliente where idCliente= '{}'
                '''.format(self.__idCliente)
            cursor.execute(query)
            lista=cursor.fetchall()

            database.commit()
        except Exception as e:
            print("Error: {}".format(e))
        finally:
            database.close()
        return lista
    def generarListaCarrito(self):
        database = sqlite3.connect("linioexp_parcial_lab3.db")  # ABRIR CONEXION CON BASE DE DATOS
        lista=[]
        try:
            cursor = database.cursor()  # OBTENER OBJETO CURSOR

            query = '''SELECT *  FROM carrito where idCliente= '{}'
                '''.format(self.__idCliente)
            cursor.execute(query)
            lista=cursor.fetchall()

            database.commit()
        except Exception as e:
            print("Error: {}".format(e))
        finally:
            database.close()
        return lista

    def iniciarSesion(self):
        database = sqlite3.connect("linioexp_parcial_lab3.db")  # ABRIR CONEXION CON BASE DE DATOS
        texto = 0
        try:
            cursor = database.cursor()  # OBTENER OBJETO CURSOR

            query = '''SELECT *  FROM cliente where (nombreusuario= '{}'or correo='{}') and password='{}'
                '''.format(self.nombreUsuario, self.correo, self.password)
            cursor.execute(query)
            lista = cursor.fetchall()
            if (len(lista) == 0):
                texto = 0
            else:
                texto = 1
                self.idCliente = lista[0][0]
                self.obtenerCliente()

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

            query = '''SELECT *  FROM cliente where nombreusuario= '{}'or correo='{}' 
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

