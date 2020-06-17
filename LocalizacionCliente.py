import sqlite3
from Localizacion import Localizacion
import Cliente as Cliente
class LocalizacionCliente(Localizacion):
    def __init__(self,idLocalizacionCliente:str=None,preterminada:bool=0,Telefono:str=None,nombre:str=None,apellidoPaterno:str=None,apellidoMaterno:str=None,cliente: Cliente=None,provincia:str=None,distrito:str=None,codigoPostal:str=None,direccion:str=None,direccionSecundaria:str=None):
        self.__idLocalizacionCliente= idLocalizacionCliente if idLocalizacionCliente is not None else self.generaridLocalizacionCliente()
        self.__preterminada=preterminada
        self.__telefono=Telefono
        self.__nombre = nombre
        self.__apellidoPaterno = apellidoPaterno
        self.__apellidoMaterno = apellidoMaterno
        self.__listaOrden=self.generarListaOrden()
        self.oCliente=cliente
        Localizacion.__init__(self,provincia,distrito,codigoPostal,direccion,direccionSecundaria)
    def __str__(self):
        return self.__idLocalizacionCliente + ": " + self.__nombre
    @property
    def idLocalizacionCliente(self):
        return self.__idLocalizacionCliente
    @property
    def preterminada(self):
        return self.__preterminada
    @property
    def telefono(self):
        return self.__telefono
    @property
    def nombre(self):
        return self.__nombre
    @property
    def apellidoPaterno(self):
        return self.__apellidoPaterno
    @property
    def apellidoMaterno(self):
        return self.__apellidoMaterno
    @telefono.setter
    def telefono(self,newTelefono):
        self.__telefono=newTelefono
    @nombre.setter
    def nombre(self, newNombre):
        self.__nombre = newNombre
    @apellidoPaterno.setter
    def apellidoPaterno(self, newApellido):
        self.__apellidoPaterno = newApellido
    @apellidoMaterno.setter
    def apellidoMaterno(self, newApellido):
        self.__apellidoMaterno = newApellido
    @preterminada.setter
    def preterminada(self, newApellido):
        self.__preterminada = newApellido
    @property
    def cliente(self):
        return self.oCliente
    @cliente.setter
    def cliente(self, new_cliente):
        self.oCliente = new_cliente


    def activarPreterminado(self):
        database = sqlite3.connect("linioexp_parcial_lab3.db")  # ABRIR CONEXION CON BASE DE DATOS


        try:
            cursor = database.cursor()  # OBTENER OBJETO CURSOR
            query = '''
                    SELECT  idLocalizacionCliente from localizacionCliente
                    WHERE idCliente = '{}' and preterminada=1
                    '''.format(self.oCliente.idCliente)
            cursor.execute(query)
            idLocal=-1
            try:
                idLocal = cursor.fetchall()[0][0]
            except:
                pass

            if(idLocal==self.__idLocalizacionCliente):
                texto="Ya estaba activado"
            else:
                texto="activacion lista"

                query = '''
                    UPDATE localizacionCliente set preterminada = 1
                    WHERE idLocalizacionCliente = '{}'
                    '''.format( self.__idLocalizacionCliente)
                cursor.execute(query)
                query = '''
                                    UPDATE localizacionCliente set preterminada = 0
                                    WHERE idLocalizacionCliente = '{}'
                                    '''.format(idLocal)
                cursor.execute(query)
            database.commit()
        except Exception as e:
            print("Error: {}".format(e))
        finally:
            database.close()  # CERRAR CONEXION CON BASE DE DATOS
        

    def generaridLocalizacionCliente(self):
        count = 0
        database = sqlite3.connect("linioexp_parcial_lab3.db")  # ABRIR CONEXION CON BASE DE DATOS
        try:
            cursor = database.cursor()  # OBTENER OBJETO CURSOR
            query = '''
            SELECT COUNT(*) FROM localizacionCliente'''
            cursor.execute(query)
            count = cursor.fetchone()
        except Exception as e:
            print("Error: {}".format(e))
        finally:
            database.close()  # CERRAR CONEXION CON BASE DE DATOS

        return "LCLI" + "0" * (4 - len(str(count[0] + 1))) + str(count[0] + 1)
    def eliminarlocalizacionCliente(self):
        database = sqlite3.connect("linioexp_parcial_lab3.db")  # ABRIR CONEXION CON BASE DE DATOS

        try:
            cursor = database.cursor()  # OBTENER OBJETO CURSOR
            query = '''
                            SELECT  idLocalizacionCliente from orden
                            WHERE idLocalizacionCliente = '{}'
                            '''.format(self.__idLocalizacionCliente)
            cursor.execute(query)
            ordenes = cursor.fetchall()


            if (len(ordenes) == 0):
              
                
                query = '''
                            DELETE FROM localizacionCliente where idLocalizacionCliente= '{}'
                            '''.format(self.__idLocalizacionCliente)
                cursor.execute(query)
                
            else:
                

                query = '''
                            UPDATE localizacionCliente set idCliente=Null
                            WHERE idLocalizacionCliente = '{}'
                            '''.format(self.__idLocalizacionCliente)
                cursor.execute(query)

            database.commit()
        except Exception as e:
            print("Error: {}".format(e))
        finally:
            database.close()  # CERRAR CONEXION CON BASE DE DATOS
            
    def actualizarlocalizacionCliente(self):
        database = sqlite3.connect("linioexp_parcial_lab3.db")  # ABRIR CONEXION CON BASE DE DATOS

        try:
            cursor = database.cursor()  # OBTENER OBJETO CURSOR
            query = '''
                                    SELECT  idLocalizacionCliente from orden
                                    WHERE idLocalizacionCliente = '{}'
                                    '''.format(self.__idLocalizacionCliente)
            cursor.execute(query)
            ordenes = cursor.fetchall()

            if (len(ordenes) == 0): #Da igual si tiene mas de una localización?
                texto = "Eliminar"
                query = '''
                        UPDATE localizacionCliente set idCliente=Null,telefono="{}",nombre="{}",  apellidoPaterno="{}",  apellidoMaterno="{}",  provincia="{}",  distrito="{}",codigoPostal="{}",direccion="{}",direccionSecundaria="{}"
                        WHERE idLocalizacionCliente = '{}'
                                                    '''.format(self.__telefono,self.__nombre, self.__apellidoPaterno, self.__apellidoMaterno,self.provincia,self.distrito,self.codigoPostal,self.direccion,self.direccionSecundaria,self.idLocalizacionCliente)
                cursor.execute(query)
        
            else:

                #localizacionCliente(telefono=self.__telefono,nombre=self.__nombre,apellidoPaterno=self.__apellidoPaterno,apellidoMaterno=self.__apellidoMaterno,provincia=self.provincia,distrito=self.distrito,codigoPostal=self.codigoPostal,direccion=self.direccion,direccionSecundaria=self.direccionSecundaria).agregarlocalizacionCliente()
                texto = "activacion lista"
                
                nuevo_id=self.generaridLocalizacionCliente()
                query = '''
                        UPDATE localizacionCliente set idCliente=Null
                        WHERE idLocalizacionCliente = '{}';
                        INSERT INTO localizacionCliente(idLocalizacionCliente,idCliente,telefono,nombre,  apellidoPaterno,  apellidoMaterno,  provincia,  distrito,codigoPostal,direccion,direccionSecundaria ) VALUES('{}', '{}', '{}', '{}','{}', '{}', '{}', '{}','{}','{}') 
                                                '''.format(self.__idLocalizacionCliente,nuevo_id,self.__telefono,self.__nombre,self.__apellidoPaterno,self.__apellidoMaterno,self.provincia,self.distrito,self.codigoPostal,self.direccion,self.direccionSecundaria)
                cursor.execute(query)

            database.commit()
        except Exception as e:
            print("Error: {}".format(e))
        finally:
            database.close() 
        return texto
    def agregarlocalizacionCliente(self):
        database = sqlite3.connect("linioexp_parcial_lab3.db")  

        try:
            cursor = database.cursor()  # OBTENER OBJETO CURSOR
            query = '''
                                        SELECT  * from localizacionCliente
                                        WHERE idCliente = '{}'
                                        '''.format(self.oCliente.idCliente)
            cursor.execute(query)
            unique = cursor.fetchall()
            self.__preterminada = 1 if len(unique) == 0 else 0
            cursor = database.cursor()  
        
           
            query = '''
                        INSERT INTO localizacionCliente(idLocalizacionCliente,telefono,nombre,  apellidoPaterno,  apellidoMaterno,  provincia,  distrito,codigoPostal,direccion,direccionSecundaria,idCliente,preterminada ) VALUES('{}', '{}', '{}', '{}','{}', '{}', '{}', '{}','{}','{}','{}','{}') 
                                                '''.format(self.__idLocalizacionCliente,self.__telefono,self.__nombre,self.__apellidoPaterno,self.__apellidoMaterno,self.provincia,self.distrito,self.codigoPostal,self.direccion,self.direccionSecundaria,self.oCliente.idCliente,self.__preterminada)
            cursor.execute(query)

            database.commit()
        except Exception as e:
            print("Error: {}".format(e))
        finally:
            database.close()  
    
    def obtenerLocalizacionCliente(self):
        database = sqlite3.connect("linioexp_parcial_lab3.db")
        try:
            cursor = database.cursor()
            query = '''
                    SELECT  * from localizacionCliente 
                    WHERE idLocalizacionCliente = '{}' 
                    '''.format(self.__idLocalizacionCliente)
            cursor.execute(query)
            lista = cursor.fetchall()
            self.__telefono=lista[1]
            self.__nombre=lista[2]
            self.__apellidoPatero=lista[3]
            self.__apellidoMaterno=lista[4]
            self.__preterminada=lista[5]
            self.provincia=lista[6]
            self.distrito=lista[7]
            self.codigoPostal=lista[8]
            self.direccion=lista[9]
            self.direccionSecundaria[10]

           
        except Exception as e:
            print("Error: {}".format(e))
        finally:
            database.close()  
    def generarListaOrden(self):
        database = sqlite3.connect("linioexp_parcial_lab3.db")  # ABRIR CONEXION CON BASE DE DATOS
        lista=[]
        try:
            cursor = database.cursor()  # OBTENER OBJETO CURSOR

            query = '''SELECT *  FROM orden where idDireccionEntrega= '{}'
                '''.format(self.__idLocalizacionCliente)
            cursor.execute(query)
            cursor.fetchall()

            database.commit()
        except Exception as e:
            print("Error: {}".format(e))
        finally:
            database.close()
        return lista
        

