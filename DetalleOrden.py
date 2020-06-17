from datetime import datetime
from Orden import Orden
from Producto import Producto
import sqlite3

#Termina
class DetalleOrden(object):
    def __init__(self, idDetalleOrden:str=None, orden:Orden=None, producto:Producto=None, cantidad: int = None, subtotal: int = None):
        self.__idDetalleOrden = idDetalleOrden if(idDetalleOrden is not None) else self.generarIdDetalleOrden()
        self.oOrden = orden
        self.oProducto = producto
        self.__cantidad = cantidad
        self.__subtotal = subtotal if(subtotal is not None) else self.calcularSubTotal()

    #Atributos
    @property
    def idDetalleOrden(self):
        return self.__idDetalleOrden
    @idDetalleOrden.setter
    def idDetalleOrden(self, new_idDetalleOrden: str):
        self.__idDetalleOrden = new_idDetalleOrden
    @property
    def orden(self):
        return self.oOrden
    @orden.setter
    def orden(self, new_orden: orden):
        self.oOrden = new_orden
    @property
    def producto(self):
        return self.oProducto
    @producto.setter
    def producto(self, new_producto:Producto):
        self.oProducto = new_producto
    @property
    def cantidad(self):
        return self.__cantidad
    @cantidad.setter
    def cantidad(self, new_cantidad: str):
        self.__cantidad = new_cantidad
    @property
    def subtotal(self):
        return self.__subtotal
    @subtotal.setter
    def subtotal(self, new_subtotal: str):
        self.__subtotal = new_subtotal
        
    #Metodos Estandar
    def generarIdDetalleOrden(self) -> str:
        count = 0
        database = sqlite3.connect("linioexp_parcial_lab3.db")  # ABRIR CONEXION CON BASE DE DATOS
        try:
            cursor = database.cursor()  # OBTENER OBJETO CURSOR
            query = '''
            SELECT COUNT(*) FROM detalleOrden'''
            cursor.execute(query)
            count = cursor.fetchone()
        except Exception as e:
            print("Error: {}".format(e))
        finally:
            database.close()  # CERRAR CONEXION CON BASE DE DATOS

        return "DET" + "0"*(4 - len(str(count[0] + 1))) + str(count[0] + 1)
    def agregarDetalleOrden(self):
        estado_op = False
        database = sqlite3.connect("linioexp_parcial_lab3.db")  # ABRIR CONEXION CON BASE DE DATOS
        try:
            cursor = database.cursor()  # OBTENER OBJETO CURSOR
            query = '''
            INSERT INTO detalleOrden(idDetalleOrden, idOrden, idProducto, cantidad, subtotal)
            VALUES ('{}', '{}', '{}', '{}','{}')'''.format(self.__idDetalleOrden,
            self.oOrden.idOrden,self.oProducto.idProducto,self.__cantidad,self.__subtotal)
            cursor.execute(query)
            database.commit()  # CONFIRMAR CAMBIOS QUERY
            estado_op = True
        except Exception as e:
            database.rollback()  # RESTAURAR ANTES DE CAMBIOS POR ERROR
            print("Error: {}".format(e))
        finally:
            database.close()  # CERRAR CONEXION CON BASE DE DATOS
        return estado_op
    def actualizarDetalleOrden(self)-> bool:
        estado_op = False
        database = sqlite3.connect("linioexp_parcial_lab3.db")
        try:
            cursor = database.cursor()
            query = '''                 
            UPDATE detalleorden
            SET idOrden = '{}', idProducto = '{}', cantidad = '{}',
            subtotal = '{}' WHERE idDetalleOrden = '{}' '''.format(self.oOrden.__idOrden, self.oProducto.__idProducto,
                       self.__cantidad, self.__subtotal,self.__idDetalleOrden)
            cursor.execute(query)
            database.commit()
            estado_op = True
        except Exception as e:
            database.rollback() 
            print("Error: {}".format(e))
        finally:
            database.close()

        return estado_op
    def eliminarDetalleOrden(self):
        database = sqlite3.connect("linioexp_parcial_lab3.db")  # ABRIR CONEXION CON BASE DE DATOS

        try:
            cursor = database.cursor()  # OBTENER OBJETO CURSOR

                
            query = '''DELETE FROM detalleOrden where idDetalleOrden= '{}'
                    '''.format(self.__idDetalleOrden)
            cursor.execute(query)


            database.commit()
        except Exception as e:
            print("Error: {}".format(e))
        finally:
            database.close()
    def obtenerDetalleOrden(self):
        database = sqlite3.connect("linioexp_parcial_lab3.db")
        try:
            cursor = database.cursor()
            query = '''
                    SELECT * from detalleOrden 
                    WHERE idDetalleOrden = '{}' 
                    '''.format(self.__idDetalleOrden)
            cursor.execute(query)
            lista = cursor.fetchoall()[0]
            self.oOrden = Orden(lista[1]).obtenerOrden()
            self.oProducto = Producto(lista[2]).obtenerProducto()
            self.__cantidad = lista[3]
            self.__subtotal = lista[4]
        except Exception as e:
            print("Error: {}".format(e))
        finally:
            database.close()  
            
    #Metodos de la clase
    def calcularSubTotal(self):
        print(self.oProducto.precio_venta)
        return self.oProducto.precio_venta * int(self.cantidad)