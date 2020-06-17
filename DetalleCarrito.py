from datetime import datetime
from Carrito import Carrito
from Producto import Producto
import sqlite3
from Cliente import Cliente

#Terminado
class DetalleCarrito(object):
    def __init__(self,idDetallecarrito:str=None, carrito:Carrito=None, producto:Producto=None, cantidad: int = None, subtotal: float = None):
        self.__idDetalleCarrito=idDetallecarrito if(idDetallecarrito is not None) else self.generarIdDetalleCarrito()
        self.oCarrito=carrito
        self.oProducto =producto

        self.__cantidad = cantidad
        self.__subtotal = subtotal if(subtotal is not None) else self.calcularSubTotal()
        
    #Atributos
    @property
    def idDetalleCarrito(self):
        return self.__idDetalleCarrito
    @idDetalleCarrito.setter
    def idDetalleCarrito(self, new_idDetallecarrito: str):
        self.__idDetalleCarrito = new_idDetallecarrito
    @property
    def carrito(self):
        return self.oCarrito
    @carrito.setter
    def carrito(self, new_carrito: carrito):
        self.oCarrito = new_carrito
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
    def generarIdDetalleCarrito(self) -> str:
        count = 0
        database = sqlite3.connect("linioexp_parcial_lab3.db")  # ABRIR CONEXION CON BASE DE DATOS
        try:
            cursor = database.cursor()  # OBTENER OBJETO CURSOR
            query = '''
            SELECT * FROM detalleCarrito'''
            cursor.execute(query)
            count = int(cursor.fetchall()[-1][0][4:9])
        except Exception as e:
            print("Error: {}".format(e))
        finally:
            database.close()  # CERRAR CONEXION CON BASE DE DATOS

        return "DETC" + "0"*(4 - len(str(count+1))) + str(count + 1)
    def agregarDetalleCarrito(self):
        database = sqlite3.connect("linioexp_parcial_lab3.db")
        try:


            cursor = database.cursor()  
           
            query = '''
                        INSERT INTO detalleCarrito(idDetalleCarrito,idProducto,idCarrito,cantidad,subtotal) VALUES('{}','{}','{}','{}','{}')
                    '''.format(self.__idDetalleCarrito ,self.oProducto.idProducto,self.oCarrito.idCarrito,self.__cantidad,self.__subtotal)
            cursor.execute(query)

            database.commit()
        except Exception as e:
            print("Error: {}".format(e))
        finally:
            database.close() 
    def actualizarDetalleCarrito(self,var=None):
        database = sqlite3.connect("linioexp_parcial_lab3.db")  
        try:
            if(var==1):
                try:
                    cursor = database.cursor()
                    query = '''
                                   SELECT * from detalleCarrito 
                                   WHERE (idProducto='{}' and idCarrito='{}') 
                                   '''.format( self.oProducto.idProducto,
                                              self.oCarrito.idCarrito)

                    cursor.execute(query)
                    lista = cursor.fetchall()[0]
                    self.__idDetalleCarrito=lista[0]
                    self.__cantidad+=lista[3]
                    self.__subtotal=self.calcularSubTotal()

                except:
                    pass
            cursor = database.cursor()
            query = '''
                    UPDATE  detalleCarrito
                    SET idCarrito="{}", idProducto="{}", cantidad="{}", subtotal="{}"
                    WHERE idDetalleCarrito = '{}' 
                    '''.format(self.oCarrito.idCarrito,self.oProducto.idProducto,self.__cantidad,self.__subtotal,self.__idDetalleCarrito)
            cursor.execute(query)
            database.commit()
            
        except Exception as e:
            print("Error: {}".format(e))
        finally:
            database.close() 
    def eliminarDetalleCarrito(self):
        database = sqlite3.connect("linioexp_parcial_lab3.db")  # ABRIR CONEXION CON BASE DE DATOS

        try:
            cursor = database.cursor()  # OBTENER OBJETO CURSOR
            query = '''DELETE FROM detalleCarrito where idDetalleCarrito= '{}'
                    '''.format(self.__idDetalleCarrito)
            cursor.execute(query)
            database.commit()
            
        except Exception as e:
            print("Error: {}".format(e))
            
        finally:
            database.close()
    def obtenerDetalleCarrito(self):
        database = sqlite3.connect("linioexp_parcial_lab3.db")
        texto=0
        try:
            if (self.oCarrito== None):
                idpro="1"
                idcar="1"
            else:
                idpro=self.oProducto.idProducto
                idcar=self.oCarrito.idCarrito

            cursor = database.cursor()
            query = '''
                    SELECT * from detalleCarrito 
                    WHERE idDetalleCarrito = '{}' or (idProducto='{}' and idCarrito='{}') 
                    '''.format(self.__idDetalleCarrito,idpro,idcar)
            cursor.execute(query)
            lista = cursor.fetchall()[0]
            texto= 0 if idpro != lista[2] else 1
            self.__idDetalleCarrito=self.__idDetalleCarrito

            self.oProducto= Producto(idProducto=lista[2])

            self.oProducto.obtenerProducto()
            self.oCarrito= Carrito(idCarrito=lista[1])
            self.oCarrito.obtenerCarrito()
            self.__cantidad=lista[3]
            self.__subtotal=lista[4]

           
        except Exception as e:
            print("Error: {}".format(e))
        finally:
            database.close()
            return texto
            
    #Metodos de la clase
    def calcularSubTotal(self):
        try:

            return float(self.oProducto.precio_venta) * int(self.__cantidad)
        except:
            return None
    def aumentarCantidad(self,num):
        self.__cantidad+=num
        self.actualizarDetalleCarrito()
    def disminuirCantidad(self,num):
        if(self.__cantidad>=num):
            self.__cantidad-=num
            self.actualizarDetalleCarrito()
        else:
            print("Error: No hay suficiente stock para disminuir")
    
    def verificarstock(self,idC):
        Cli=Cliente(idCliente=idC).generarListaCarrito()[0][0]

        detalles=Carrito(idCarrito=Cli).generarListaDetalleCarrito()

        veri=1
        for det in detalles:
            pro=Producto(idProducto=det[2])
            pro.obtenerProducto()

            if int(det[3])>int(pro.stock):
                self.idDetalleCarrito=det[0]
                self.obtenerDetalleCarrito()

                self.cantidad=pro.stock
                if(pro.stock==0):
                    self.eliminarDetalleCarrito()
                else:
                    self.actualizarDetalleCarrito()
                veri=0
        return veri