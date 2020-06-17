import sqlite3
from Comercio import Comercio

CATEGORIAS={"TEXTILES":"T", "ELECTRODOMESTICOS": "E", "CONSUMIBLES": "C"}

#Terminado
class Producto(object):
    def __init__(self,comercio:Comercio=None,idProducto:str=None,nombre:str=None,precio: float=None,stock:int=None,descuento:float=None,categoria:str=None,descripcion:str=None):
        self.__idProducto=idProducto if idProducto is not None else self.generarIdProducto()
        self.__nombre=nombre
        self.__precio=precio 
        self.__stock=stock
        self.__descuento=descuento
        self.__categoria=categoria
        self.__descripcion=descripcion
        self.__precio_venta=self.calcularPrecioVenta()
        self.__listaDet=list()
        self.__listaDetCar = list()
        self.oComercio=comercio
    
    #Atributos
    @property
    def idProducto(self):
        return self.__idProducto
    @property
    def nombre(self):
        return self.__nombre
    @nombre.setter
    def nombre(self,newNombre):
        self.__nombre=newNombre
    @property
    def precio(self):
        return self.__precio
    @precio.setter
    def precio(self,newPrecio):
        self.__precio=newPrecio
    @property
    def stock(self):
        return self.__stock
    @stock.setter
    def stock(self, newStock):
        self.__stock = newStock
    @property
    def descuento(self):
        return self.__descuento
    @descuento.setter
    def descuento(self,newDescuento):
        self.__descuento=newDescuento
    @property
    def categoria(self):
        return self.__categoria
    @categoria.setter
    def categoria(self,newCategoria):
        self.__descuento=newCategoria
    @property
    def comercio(self):
        return self.oComercio
    @comercio.setter
    def comercio(self,newComercio):
        self.comercio=newComercio
    @property
    def precio_venta(self):
        return self.__precio_venta
    @precio_venta.setter
    def precio_venta(self,new):
        self.__precio_venta=new

    @property
    def descripcion(self):
        return self.__descripcion



    @descripcion.setter
    def descripcion(self, new):
        self.__descripcion = new

    #Metodos de Clase
    def generarIdProducto(self):
        count = 0
        database = sqlite3.connect("linioexp_parcial_lab3.db")  # ABRIR CONEXION CON BASE DE DATOS
        try:
            cursor = database.cursor()  # OBTENER OBJETO CURSOR
            query = '''
            SELECT COUNT(*) FROM producto'''
            cursor.execute(query)
            count = int(cursor.fetchone()[0])
        except Exception as e:
            print("Error: {}".format(e))
        finally:
            database.close()  # CERRAR CONEXION CON BASE DE DATOS

        return "PROD" + "0" * (4 - len(str(count + 1))) + str(count + 1)
    def agregarProducto(self):
        estado_op = False
        database = sqlite3.connect("linioexp_parcial_lab3.db")
        try:
            cursor = database.cursor() 
            query = '''
            INSERT INTO producto(idProducto,nombre,precio,stock,descuento,categoria,idComercio,descripcion)
            VALUES ('{}','{}','{}','{}','{}','{}','{}','{}')'''.format(self.__idProducto,
                self.__nombre,self.__precio,self.__stock,self.__descuento,self.__categoria,self.oComercio.idComercio,self.__descripcion)
            cursor.execute(query)
            database.commit() 
            estado_op = True

        except Exception as e:
            database.rollback()
            print("Error: {}".format(e))
        finally:
            database.close()
        return estado_op
    def actualizarProducto(self):
        database = sqlite3.connect("linioexp_parcial_lab3.db")  
        try:

            cursor = database.cursor()
            query = '''
                    UPDATE  producto set nombre = '{}',precio = '{}',stock = '{}',descuento = '{}',categoria = '{}',descripcion='{}'
                    WHERE idProducto = '{}'
                    '''.format(self.__nombre,self.__precio,self.__stock,self.__descuento,self.__categoria,self.__descripcion,self.__idProducto)
            cursor.execute(query)
            database.commit()
            cursor = database.cursor()
            print(query)
            query = '''
                                UPDATE  detallecarrito set subtotal = '{}'
                                WHERE idProducto = '{}'
                                '''.format(self.calcularPrecioVenta(),self.__idProducto)
            cursor.execute(query)
            database.commit()
            
        except Exception as e:
            print("Error: {}".format(e))
        finally:
            database.close()  
    def eliminarProducto(self):
        database = sqlite3.connect("linioexp_parcial_lab3.db")  # ABRIR CONEXION CON BASE DE DATOS
        try:
            cursor = database.cursor()  # OBTENER OBJETO CURSOR
            query = '''DELETE FROM producto where idProducto= '{}'
                    '''.format(self.__idProducto)
            cursor.execute(query)
            database.commit()
        except Exception as e:
            print("Error: {}".format(e))
        finally:
            database.close()
    def obtenerProducto(self):
        database = sqlite3.connect("linioexp_parcial_lab3.db")
        try:
            cursor = database.cursor()
            query = '''
                    SELECT * from producto
                    WHERE idProducto = '{}' 
                    '''.format(self.__idProducto)
            cursor.execute(query)
            lista = cursor.fetchall()[0]

            self.__nombre=lista[1]
            self.__precio=lista[2]
            self.__stock=lista[3]
            self.__descuento=lista[4]
            self.__categoria=lista[5]
            self.oComercio=Comercio(idComercio=lista[6])
            self.oComercio.obtenerComercio()
            self.__precio_venta=self.calcularPrecioVenta()
            self.__descripcion=lista[7]
        
            
            #self.precio_venta=self.calcularPrecioVenta()
            
        
           
        except Exception as e:
            print("Error: {}".format(e))
        finally:
            database.close()  
    
    #Metodos Estandar
    def calcularPrecioVenta(self):
        try:
            self.__descuento= 0 if self.__descuento is None else self.__descuento
            d=(self.__precio * (1-self.__descuento))
            return d
        except:
            return None

    def generarListaDet(self):
        pass
    def generarListaDetCar(self):
        pass

    def obtenerlistaProducto(self):
        database = sqlite3.connect("linioexp_parcial_lab3.db")
        lista=[]
        try:
            cursor = database.cursor()
            query = '''
                    SELECT * from producto
                    WHERE idProducto = '{}' 
                    '''.format(self.__idProducto)
            cursor.execute(query)
            lista = cursor.fetchall()[0]

            self.__precio = lista[2]

            self.__descuento = lista[4]
            lista=[x for x in lista]
            lista.append(self.calcularPrecioVenta())



            #



        except Exception as e:
            print("Error: {}".format(e))
        finally:
            database.close()
            return lista
    def filtrarProducto(self, alto=10000000, bajo=-1, comercio=0, categoria=[], pre=None, alf=None):
        database = sqlite3.connect("linioexp_parcial_lab3.db")  # ABRIR CONEXION CON BASE DE DATOS

        try:
            switch = 0 if comercio is 0 else 1
            cursor = database.cursor()  # OBTENER OBJETO CURSOR
            query = '''select * FROM producto where precio< {} and precio> {} '''.format(alto,
                                                                                         bajo) + switch * " and idComercio='{}' ".format(
                comercio)
            if (len(categoria) != 0):
                a = 0
                query += " and ("
                for e in categoria:
                    query += "or" * a + " categoria='{}'".format(e)
                a = 1
                query += ")"

            if (pre is not None or alf is not None):
                query += " order by"
                if (pre is not None and alf is None):
                    query += " precio " + pre
                elif (alf is not None and pre is None):
                    query += " nombre " + alf
                else:
                    query += " precio {} , nombre {} ".format(pre, alf)
            print(query)
            cursor.execute(query)
            Productos = cursor.fetchall()
        except Exception as e:
            print("Error: {}".format(e))
        finally:
            database.close()
            return Productos, query

    def buscarProducto(self, alto=1000000000, bajo=-1, comercio=0, categoria=[], pre=None, alf=None, Palabra=None,num=1):
        database = sqlite3.connect("linioexp_parcial_lab3.db")  # ABRIR CONEXION CON BASE DE DATOS
        Product=[]
        try:
            switch = 0 if Palabra is None else 1
            Pro, query = self.filtrarProducto(categoria=categoria, bajo=bajo, pre=pre, comercio=comercio, alf=alf,
                                              alto=alto)

            cursor = database.cursor()  # OBTENER OBJETO CURSOR
            query = '''select * from (select *,(ROW_NUMBER() OVER (ORDER BY 1)) as N FROM ({}) '''.format(
                query) + switch *( ''' where (nombre like '%{}%' or descripcion like '%{}%' '''.format(Palabra,Palabra)) +''' ))where N>{} and N<={} '''.format(
                 (num - 1) * 10, num * 10)

            cursor.execute(query)
            Product = cursor.fetchall()

            print(query)
        except Exception as e:
            print("Error: {}".format(e))
        finally:
            database.close()
            return Product
    def CantidadVendidos(self):
        database = sqlite3.connect("linioexp_parcial_lab3.db")
        cantidad = 0
        try:
            cursor = database.cursor()
            query = '''
                            SELECT sum(cantidad) from detalleorden
                            WHERE idProducto = '{}' 
                            '''.format(self.__idProducto)
            cursor.execute(query)
            cantidad = cursor.fetchall()[0]
            print(cantidad)
            cantidad= (0,) if cantidad[0] is None else cantidad




            #



        except Exception as e:
            print("Error: {}".format(e))
        finally:
            database.close()
            return cantidad