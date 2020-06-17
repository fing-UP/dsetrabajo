import datetime
from Cliente import Cliente
import sqlite3

#Completamente revisada solo faltaria obtener
class Tarjeta(object):
    def __init__(self,cliente:Cliente=None, numTarjeta: str = None, proveedor: str = None,fechaVencimiento:str= None,nombrePropetario:str=None,numSec:str=None,preterminado:bool=0):
        self.__numTarjeta =numTarjeta
        self.__proveedor = proveedor
        self.oCliente=cliente
        self.__listaOrden=list()
        self.__fechaVencimiento=fechaVencimiento
        self.__nombrePropetario=nombrePropetario
        self.__numSec=numSec
        self.__preterminado=preterminado
    def __str__(self):
        return self.numTarjeta
        
    @property
    def numTarjeta(self):
        return self.__numTarjeta
    @numTarjeta.setter
    def numTarjeta(self, new_numTarjeta):
        self.__numTarjeta = new_numTarjeta
    @property
    def proveedor(self):
        return self.__proveedor
    @proveedor.setter
    def banco(self, new_proveedor):
        self.__banco = new_proveedor
    @property
    def fechaVencimiento(self):
        return self.__fechaVencimiento
    @property 
    def nombrePropetario(self):
        return self.__nombrePropetario
    @nombrePropetario.setter
    def nombrePropetario(self,new_nombre):
        self.__nombrePropetario=new_nombre
    @fechaVencimiento.setter
    def fechaVencimiento(self,new_fecha):
        self.__fechaVencimiento=new_fecha
    @property 
    def numSec(self):
        return self.__numSec
    @numSec.setter
    def numSec(self,new_Sec):
        self.__numSec=new_Sec
    @property
    def preterminado(self):
        return self.__preterminado
    @property
    def cliente(self):
        return self.oCliente
    @cliente.setter
    def cliente(self,newCliente):
        self.oCliente=newCliente
    @preterminado.setter
    def preterminado(self,new):
        self.__preterminado = new

    #Metodos Estandar
    def agregarTarjeta(self):
        database = sqlite3.connect("linioexp_parcial_lab3.db")  

        try:
            cursor = database.cursor()  # OBTENER OBJETO CURSOR
            query = '''
                            SELECT  numTarjeta from Tarjeta
                            WHERE idCliente = '{}'
                            '''.format(self.oCliente.idCliente)
            cursor.execute(query)
            unique = cursor.fetchall()
            self.__preterminado=1 if len(unique)==0 else 0
            cursor = database.cursor()  
           
            insert = '''
                        INSERT INTO tarjeta(numTarjeta,idCliente,proveedor,numSec,fechaVencimiento,nombrePropetario,preterminado) VALUES('{}', '{}', '{}', '{}','{}', '{}','{}') 
                                                '''.format(self.__numTarjeta,self.oCliente.idCliente,self.__proveedor,self.__numSec,self.__fechaVencimiento,self.__nombrePropetario,self.__preterminado)
            cursor.execute(insert)

            """
            if(len(cursor.fetchall())==1):
                self.activarPreterminado()
            else:
                if(self.__preterminado==1):
                    self.activarPreterminado()"""
                    
                
            
            

            database.commit()
        except Exception as e:
            print("Error: {}".format(e))
        finally:
            database.close()  
    def actualizarTarjeta(self):
        database = sqlite3.connect("linioexp_parcial_lab3.db")  # ABRIR CONEXION CON BASE DE DATOS


        try:
            cursor = database.cursor()  # OBTENER OBJETO CURSOR

            update = '''
                    UPDATE tarjeta set nombrePropetario='{}',numSec='{}',fechaVencimiento='{}'
                                    WHERE numTarjeta = '{}'
                    '''.format(self.__nombrePropetario,self.numSec,self.__fechaVencimiento ,self.__numTarjeta)
            cursor.execute(update)
                
            database.commit()
            if self.__preterminado is 1:
                self.activarPreterminado()
            
                
        except Exception as e:
            print("Error: {}".format(e))
        finally:
            database.close()
    def eliminarTarjeta(self):
        database = sqlite3.connect("linioexp_parcial_lab3.db")  # ABRIR CONEXION CON BASE DE DATOS

        try:
            cursor = database.cursor()  # OBTENER OBJETO CURSOR
            query = '''
                            SELECT  numTarjeta from orden
                            WHERE numTarjeta = '{}'
                            '''.format(self.__numTarjeta)
            cursor.execute(query)
            ordenes = cursor.fetchall()


            if (len(ordenes) == 0):
              
                
                query = '''
                            DELETE FROM tarjeta where numTarjeta= '{}'
                            '''.format(self.__numTarjeta)
                cursor.execute(query)
                
            else:
                

                query = '''
                            UPDATE tarjeta set idCliente=Null
                            WHERE  numTarjeta = '{}'
                            '''.format(self.__numTarjeta)
                cursor.execute(query)

            database.commit()
        except Exception as e:
            print("Error: {}".format(e))
        finally:
            database.close()  # CERRAR CONEXION CON BASE DE DATOS       
    def obtenerTarjeta(self):
        database = sqlite3.connect("linioexp_parcial_lab3.db")

        try:
            cursor = database.cursor()
            query = '''
                    SELECT * from tarjeta 
                    WHERE numTarjeta = '{}' 
                    '''.format(self.__numTarjeta)
            cursor.execute(query)
            lista = cursor.fetchall()[0]
            self.oCliente=Cliente(idCliente=lista[1])
            self.oCliente.obtenerCliente()

            self.__proveedor=lista[2]
            self.__numSec=lista[3]
            self.__fechaVencimiento=lista[4]
            self.__preterminado=lista[5]
            
           
        except Exception as e:
            print("Error: {}".format(e))
        finally:
            database.close() 
            
    #Metodo de la Clase
    def obtenerTarjetaOculta(self):
        e=self.__numTarjeta
        return ( ''' *** {}{} '''.format(e[-4:-1],e[-1]))
    def activarPreterminado(self):
        database = sqlite3.connect("linioexp_parcial_lab3.db")  # ABRIR CONEXION CON BASE DE DATOS


        try:
            cursor = database.cursor()  # OBTENER OBJETO CURSOR
            query = '''
                    SELECT  numTarjeta from tarjeta
                    WHERE idCliente = '{}' and preterminado=1
                    '''.format(self.oCliente.idCliente)
            cursor.execute(query)
            numtarjeta = cursor.fetchone()

            if(numtarjeta==self.__numTarjeta):
                pass
                
            else:
                

                query = '''
                    UPDATE tarjeta set preterminado = 1
                                    WHERE numTarjeta = '{}'
                    '''.format( self.__numTarjeta)
                cursor.execute(query)
                query = '''
                                    UPDATE tarjeta set preterminado = 0
                                    WHERE numTarjeta = '{}'
                                    '''.format(numtarjeta[0])
                cursor.execute(query)
            database.commit()
        except Exception as e:
            print("Error: {}".format(e))
        finally:
            database.close()  
    