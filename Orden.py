import datetime
import sqlite3
from Cliente import Cliente
from Tarjeta import Tarjeta
from Repartidor import Repartidor
from LocalizacionCliente import LocalizacionCliente

#Terminado
class Orden(object):
    LISTA_ESTADO = {"NUEVO": "N", "TRANSPORTANDO": "T", "FACTURADO": "F", "COBRADO": "C", "CANCELADO": "X", "DEVUELTO": "D"}
    LISTA_METODOPAGO = {"EFECTIVO": "E", "TARJETA": "T"}

    def __init__(self, idOrden: str = None, cliente: Cliente = None, repartidor:Repartidor = None, 
                direccionEntrega: LocalizacionCliente = None, metodoPago: str = None, tarjeta: Tarjeta = None,
                fechaRegistro: datetime = None, fechaEntrega: datetime = None, estado: str = None,
                tarifa: float = None):
        self.__idOrden = idOrden if (idOrden != None) else self.generarIdOrden()
        self.oCliente = cliente
        self.oRepartidor = repartidor
        self.oDireccionEntrega = direccionEntrega
        self.__metodoPago = metodoPago if (metodoPago != None) else "T" if (tarjeta != None) else "E"
        self.oTarjeta = tarjeta
        self.__fechaRegistro = fechaRegistro if (fechaRegistro != None) else datetime.datetime.now()
        self.__fechaEntrega = fechaEntrega if (fechaEntrega != None) else datetime.datetime.now() + datetime.timedelta(days=1)
        self.__estado = estado if (estado != None) else "N"
        self.__tarifa = tarifa if (tarifa != None) else self.calcular_tarifa()

        def __str__(self):
            return self.idOrden

    #Atributos
    @property
    def idOrden(self):
        return self.__idOrden
    @idOrden.setter
    def idOrden(self, new_idOrden):
        self.__idOrden = new_idOrden
    @property
    def cliente(self):
        return self.oCliente
    @cliente.setter
    def cliente(self, new_cliente):
        self.oCliente = new_cliente
    @property
    def repartidor(self):
        return self.oRepartidor
    @repartidor.setter
    def repartidor(self, new_repartidor):
        self.oRepartidor = new_repartidor
    @property
    def direccionEntrega(self):
        return self.oDireccionEntrega
    @direccionEntrega.setter
    def direccionEntrega(self, new_direccionEntrega):
        self.oDireccionEntrega = new_direccionEntrega
    @property
    def metodoPago(self):
        return self.__metodoPago
    @metodoPago.setter
    def metodoPago(self, new_metodoPago):
        self.__metodoPago = new_metodoPago
    @property
    def tarjeta(self):
        return self.oTarjeta
    @tarjeta.setter
    def tarjeta(self, new_tarjeta):
        self.oTarjeta = new_tarjeta
    @property
    def fechaRegistro(self):
        return self.__fechaRegistro
    @fechaRegistro.setter
    def fechaRegistro(self, new_fechaRegistro):
        self.__fechaRegistro = new_fechaRegistro
    @property
    def fechaEntrega(self):
        return self.__fechaEntrega
    @fechaEntrega.setter
    def fechaEntrega(self, new_fechaEntrega):
        self.__fechaEntrega = new_fechaEntrega
    @property
    def estado(self):
        return self.__estado
    @estado.setter
    def estado(self, new_estado):
        self.__estado = new_estado
    @property
    def tarifa(self):
        return self.__tarifa
    @tarifa.setter
    def tarifa(self, new_tarifa):
        self.__tarifa = new_tarifa
    
    #Metodos Estandar
    def generarIdOrden(self) -> str:
        count = 0
        database = sqlite3.connect("linioexp_parcial_lab3.db")  # ABRIR CONEXION CON BASE DE DATOS
        try:
            cursor = database.cursor()  # OBTENER OBJETO CURSOR
            query = '''
            SELECT COUNT(*) FROM orden'''
            cursor.execute(query)
            count = cursor.fetchone()
        except Exception as e:
            print("Error: {}".format(e))
        finally:
            database.close()  # CERRAR CONEXION CON BASE DE DATOS

        return "ORD" + "0" * (4 - len(str(count[0] + 1))) + str(count[0] + 1)
    def agregarOrden(self):
        database = sqlite3.connect("linioexp_parcial_lab3.db")
        try:
            cursor = database.cursor()
            print(4)
            query = '''
            INSERT INTO orden(idOrden,idCliente,idRepartidor,idDireccionEntrega,
            metodoPago,numTarjeta,fechaRegistro,fechaEntrega,estado,tarifa) 
            VALUES('{}', '{}', '{}', '{}','{}', '{}', '{}','{}', '{}','{}') 
            '''.format(self.__idOrden,self.oCliente.idCliente,
                        None if (self.oRepartidor==None) else self.oRepartidor.idRepartidor,
                        self.oDireccionEntrega.idLocalizacionCliente,
                        self.__metodoPago,
                        None if (self.oTarjeta==None) else self.oTarjeta.numTarjeta,
                        self.__fechaRegistro,
                        self.__fechaEntrega,self.__estado,self.__tarifa)
            cursor.execute(query)
            print(444)
            database.commit()
        except Exception as e:
            print("Error: {}".format(e))
        finally:
            database.close()
    def actualizarOrden(self) -> bool:
        estado_op = False
        database = sqlite3.connect("linioexp_parcial_lab3.db")

        try:
            cursor = database.cursor()
            query = '''                 
            UPDATE orden
            SET idOrden = '{}',idCliente = '{}',idRepartidor = '{}',idDireccionEntrega = '{}',
            metodoPago = '{}',idTarjeta = '{}',fechaRegistro = '{}',fechaEntrega = '{}',
            estado = '{}',tarifa = '{}' 
            WHERE idOrden = '{}' '''.format(
                self.__idOrden, self.oCliente,self.oRepartidor,self.oDireccionEntrega,
                self.__metodoPago,self.oTarjeta,self.__fechaRegistro,self.__fechaEntrega,
                "S",self.__tarifa)
            cursor.execute(query)
            database.commit()
            estado_op = True
        except Exception as e:
            database.rollback()  # RESTAURAR ANTES DE CAMBIOS POR ERROR
            print("Error: {}".format(e))
        finally:
            database.close()  # CERRAR CONEXION CON BASE DE DATOS
        return estado_op
    def eliminarOrden(self):
        database = sqlite3.connect("linioexp_parcial_lab3.db")  # ABRIR CONEXION CON BASE DE DATOS
        try:
            cursor = database.cursor()
            query = '''DELETE FROM orden where idOrden= '{}'
                    '''.format(self.__idOrden)
            cursor.execute(query)
            database.commit()
        except Exception as e:
            print("Error: {}".format(e))
        finally:
            database.close()
    def obtenerOrden(self):
        database = sqlite3.connect("linioexp_parcial_lab3.db")
        try:
            cursor = database.cursor()
            query = '''
                    SELECT * from orden
                    WHERE idOrden = '{}' 
                    '''.format(self.__idOrden)
            cursor.execute(query)
            lista = cursor.fetchall()[0]
            self.oCliente = Cliente(lista[1]).obtenerCliente()
            self.oRepartidor = Repartidor(lista[2]).obtenerRepartidor()
            self.oDireccionEntrega = LocalizacionCliente(lista[3]).obtenerLocalizacionCliente()
            self.__metodoPago = lista[4]
            self.oTarjeta = Tarjeta(lista[5]).obtenerTarjeta()
            self.__fechaRegistro = lista[6]
            self.__fechaEntrega = lista[7]
            self.__estado = lista[8]
            self.__tarifa = lista[9]
           
        except Exception as e:
            print("Error: {}".format(e))
        finally:
            database.close()  
    
    #Metodos de la Clase
    def calcular_tarifa(self):
        database = sqlite3.connect("linioexp_parcial_lab3.db")  # ABRIR CONEXION CON BASE DE DATOS
        tarifa = 0
        try:
            cursor = database.cursor()  # OBTENER OBJETO CURSOR
            query = '''
            SELECT subtotal from detalleOrden
            WHERE idOrden = '{}'
            '''.format(self.__idOrden)
            cursor.execute(query)
            subtotales = cursor.fetchall()
            for i in subtotales:
                tarifa = tarifa + i[0]
            query = '''
            UPDATE orden set tarifa = '{}'
            WHERE idOrden = '{}'
            '''.format(tarifa, self.idOrden)
            cursor.execute(query)
            database.commit()
        except Exception as e:
            print("Error: {}".format(e))
        finally:
            database.close()  # CERRAR CONEXION CON BASE DE DATOS
        return tarifa
    def listar_orden_estado(self):
        database = sqlite3.connect("linioexp_parcial_lab3.db")  # ABRIR CONEXION CON BASE DE DATOS
        can = 1
        try:
            cursor = database.cursor()  # OBTENER OBJETO CURSOR
            query = '''
                    SELECT idOrden, estado from orden'''
            cursor.execute(query)
            corden = cursor.fetchall()
            for ped in corden:
                print(str(can) + ")" + ped[0] + ". Estado: " + ped[1])
                can = can + 1
        except Exception as e:
            print("Error: {}".format(e))
        finally:
            database.close()  # CERRAR CONEXION CON BASE DE DATOS
    def asignar_repartidor(self, rep):
        database = sqlite3.connect("linioexp_parcial_lab3.db")  # ABRIR CONEXION CON BASE DE DATOS
        try:
            cursor = database.cursor()  # OBTENER OBJETO CURSOR
            query = '''
            Update orden set repartidor = '{}' 
            where idOrden = '{}' '''.format(rep, self.idOrden)
            cursor.execute(query)
            database.commit()
        except Exception as e:
            print("Error: {}".format(e))
        finally:
            database.close()  # CERRAR CONEXION CON BASE DE DATOS
    def cancelar_Orden(self):
        database = sqlite3.connect("linioexp_parcial_lab3.db")


        try:
            cursor = database.cursor()
            query = '''
                    update orden set estado='X'
                    WHERE idOrden='{}' 
                    '''.format(self.__idOrden)
            print(query)
            cursor.execute(query)
            database.commit()

           
        except Exception as e:
            print("Error: {}".format(e))
        finally:
            database.close()  
    def elegirMetodoPago(self):
        pass
    def transportar(self):
        from datetime import datetime

        database = sqlite3.connect("linioexp_parcial_lab3.db")  # ABRIR CONEXION CON BASE DE DATOS
        can = 1
        try:
            cursor = database.cursor()  # OBTENER OBJETO CURSOR
            query = '''
                            SELECT idOrden,fechaRegistro, estado from orden where estado= 'C' '''
            cursor.execute(query)
            corden = cursor.fetchall()
            try:
                for ped in corden:
                    self.__idOrden=ped[0]
                    self.obtenerOrden()
                    date_string=self.__fechaRegistro.split(".")[0]
                    if (datetime.now()-datetime.fromisoformat(date_string)).days>4 and self.__estado=='C':
                        self.__estado='T'

            except:
                pass
            try:
                cursor = database.cursor()  # OBTENER OBJETO CURSOR
                query = '''
                                            SELECT idOrden,fechaRegistro, estado from orden where estado= 'T' '''
                cursor.execute(query)
                corden = cursor.fetchall()
                for ped in corden:
                    self.__idOrden = ped[0]
                    self.obtenerOrden()
                    date_string = self.__fechaRegistro.split(".")[0]

                    if (datetime.now() - datetime.fromisoformat(date_string)).days > 5 and self.__estado == 'T':
                        self.__estado = 'E'
            except:
                pass


        except Exception as e:
            print("Error: {}".format(e))
        finally:
            database.close()  # CERRAR CONEXION CON BASE DE DATOS
