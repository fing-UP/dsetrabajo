import datetime
import sqlite3
from Cliente import Cliente
from Orden import Orden
from DetalleOrden import DetalleOrden
from Producto import Producto
from Tarjeta import Tarjeta


#Termina
class Carrito(object):
    def __init__(self,idCarrito:str=None,cliente:Cliente=None,importeTotal:float=None):
        self.__idCarrito=idCarrito if idCarrito is not None else self.generarIdCarrito()
        self.oCliente=cliente
        self.__importeTotal=importeTotal if (importeTotal != None) else self.calcularImporte()
        self.__listaDetalleCarrito=self.generarListaDetalleCarrito()
        
    #Atributos
    @property
    def idCarrito(self):
        return self.__idCarrito
    @idCarrito.setter
    def idCarrito(self,newIdCarrito):
        self.__idCarrito=newIdCarrito
    @property
    def cliente(self):
        return self.oCliente
    @cliente.setter
    def cliente(self,newcliente:Cliente):
        self.oCliente = newcliente
    @property
    def importeTotal(self):
        return self.__importeTotal
    @importeTotal.setter
    def importeTotal(self, newimporteTotal):
        self.__importeTotal = newimporteTotal
        
    #Metodos Estandar
    def generarIdCarrito(self) -> str:
        count = 0
        database = sqlite3.connect("linioexp_parcial_lab3.db")  # ABRIR CONEXION CON BASE DE DATOS
        try:
            cursor = database.cursor()  # OBTENER OBJETO CURSOR
            query = '''
            SELECT COUNT(*) FROM carrito'''
            cursor.execute(query)
            count = cursor.fetchone()
        except Exception as e:
            print("Error: {}".format(e))
        finally:
            database.close()  # CERRAR CONEXION CON BASE DE DATOS

        return "CAR" + "0"*(4 - len(str(count[0] + 1))) + str(count[0] + 1)
    def agregarCarrito(self):
        database = sqlite3.connect("linioexp_parcial_lab3.db")  

        try:
            cursor = database.cursor()  
           
            query = '''
                        INSERT INTO carrito(idCarrito,idCliente,importeTotal) VALUES('{}','{}','{}')
                    '''.format(self.__idCarrito,self.oCliente.idCliente,self.importeTotal)
            cursor.execute(query)

            database.commit()
        except Exception as e:
            print("Error: {}".format(e))
        finally:
            database.close() 
    def actualizarCarrito(self):
        database = sqlite3.connect("linioexp_parcial_lab3.db")  
        try:

            cursor = database.cursor()
            query = '''
                    UPDATE carrito set idCliente="{}", importeTotal="{}"
                    WHERE idCarrito = '{}'
                    '''.format(self.oCliente.__idCliente,self.__importeTotal,self.__idCarrito)
            cursor.execute(query)
            database.commit()
            
        except Exception as e:
            print("Error: {}".format(e))
        finally:
            database.close()  
    def eliminarCarrito(self):
        database = sqlite3.connect("linioexp_parcial_lab3.db")  # ABRIR CONEXION CON BASE DE DATOS
        try:
            self.limpiarCarrito()
            cursor = database.cursor()  # OBTENER OBJETO CURSOR
            query = '''DELETE FROM carrito where idCarrito= '{}'
                    '''.format(self.__idCarrito)
            cursor.execute(query)
            database.commit()
        except Exception as e:
            print("Error: {}".format(e))
        finally:
            database.close()
            self.obtenerCarrito(self.__idCarrito)
    def obtenerCarrito(self):
        database = sqlite3.connect("linioexp_parcial_lab3.db")
        try:
            cursor = database.cursor()
            query = '''
                    SELECT * from carrito 
                    WHERE idCarrito = '{}' 
                    '''.format(self.__idCarrito)
            cursor.execute(query)
            lista = cursor.fetchall()[0]
            self.__idCarrito=lista[0]
            cli=Cliente(idCliente=lista[1])
            cli.obtenerCliente()
            self.oCliente=cli
            self.__importeTotal=self.calcularImporte()
           
        except Exception as e:
            print("Error: {}".format(e))
        finally:
            database.close()  
    
    #Metodos de la clase
    """
    def comprarCarrito(self,Lugar,Tarjeta=None,pagoEfectivo=None):
        if pagoEfectivo is not None:
            metPago="EFECTIVO"
        else:
            metPago="TARJETA"
        database = sqlite3.connect("linioexp_parcial_lab3.db")
        try:

            cursor = database.cursor()
            query = '''                 
            select * from detalleCarrito where idCarrito={}'
            '''.format(self.__idCarrito)
            cursor.execute(query)
            CartDet=cursor.fetchall(query) #la shit de abajo no funciona asi que flojera
            Ordenes=Orden(cliente=self.oCliente,fechaCreacion=datetime.datetime.now(),estado='Pendiente',ubicacion=Lugar,tarifa=self.__importeTotal,tarjeta=Tarjeta,metodoPago=metPago) #arreglar pago efectivo
            detalle=Ordenes.IDorden
            for e in CartDet:
                
                cursor = database.cursor()  
           
                query = '''
                        INSERT INTO detalleOrden(idProducto,cantidad,subtotal,idOrden) VALUES('{}', '{}', '{}', '{}') #quitar id de detalle
                                                '''.format(e[2],e[3],e[4],detalle)
                cursor.execute(query)

                database.commit()
            
            
            database.commit()
            self.limpiarCarrito()
            
        except Exception as e:
            database.rollback()  # RESTAURAR ANTES DE CAMBIOS POR ERROR
            print("Error: {}".format(e))
        finally:
            database.close()  # CERRAR CONEXION CON BASE DE DATOS
    """
    def limpiarCarrito(self):
        database = sqlite3.connect("linioexp_parcial_lab3.db")  # ABRIR CONEXION CON BASE DE DATOS

        try:
            cursor = database.cursor()  # OBTENER OBJETO CURSOR
                
            query = '''DELETE FROM detalleCarrito where idCarrito= '{}'
                    '''.format(self.__idCarrito)
            cursor.execute(query)

            database.commit()
            self.obtenerCarrito()
        except Exception as e:
            print("Error: {}".format(e))
        finally:
            database.close()
            
    def generarListaDetalleCarrito(self):
        database = sqlite3.connect("linioexp_parcial_lab3.db")  # ABRIR CONEXION CON BASE DE DATOS
        lista=[]
        try:
            cursor = database.cursor()  # OBTENER OBJETO CURSOR

                
            query = '''SELECT *  FROM detalleCarrito where idCarrito= '{}'
                    '''.format(self.__idCarrito)
            cursor.execute(query)
            lista=cursor.fetchall()


            database.commit()
        except Exception as e:
            print("Error: {}".format(e))
        finally:
            database.close()
        return lista
    def comprarCarrito(self,Lugar,tarjeta=None):
        if tarjeta is None:
            metPago="EFECTIVO"
            nuevaOrden = Orden(cliente=self.oCliente, direccionEntrega=Lugar, metodoPago=metPago,
                               tarifa=self.__importeTotal, estado="C")
        else:
            metPago="TARJETA"
            nuevaOrden = Orden(cliente=self.oCliente, direccionEntrega=Lugar, metodoPago=metPago,
                               tarifa=self.__importeTotal, estado="C",tarjeta=Tarjeta(numTarjeta=tarjeta))


        nuevaOrden.agregarOrden()
        for dc in self.__listaDetalleCarrito:

            pro=Producto(idProducto=dc[2])
            pro.obtenerProducto()
            pro.stock=pro.stock-int(dc[3])

            pro.actualizarProducto()
            nuevoDetOrden=DetalleOrden(orden=nuevaOrden,producto=pro,cantidad=dc[3])
            nuevoDetOrden.agregarDetalleOrden()

        self.limpiarCarrito()
    def calcularImporte(self):
        database = sqlite3.connect("linioexp_parcial_lab3.db")  # ABRIR CONEXION CON BASE DE DATOS
        tarifa = 0
        try:
            cursor = database.cursor()  # OBTENER OBJETO CURSOR
            query = '''
            SELECT subtotal from detalleCarrito
            WHERE idCarrito = '{}'
            '''.format(self.__idCarrito)
            cursor.execute(query)
            subtotales = cursor.fetchall()
            for i in subtotales:
                tarifa = tarifa + i[0]
            query = '''
            UPDATE carrito set importetotal = '{}'
            WHERE idCarrito = '{}'
            '''.format(tarifa, self.__idCarrito)
            cursor.execute(query)
            database.commit()
        except Exception as e:
            print("Error: {}".format(e))
        finally:
            database.close()  # CERRAR CONEXION CON BASE DE DATOS
        return tarifa

