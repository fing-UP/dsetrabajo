import sqlite3
from Localizacion import Localizacion
import Comercio as Comercio
class LocalizacionComercio(Localizacion):
    def __init__(self,idLocalizacionComercio:str=None,comercio: Comercio=None,provincia:str=None,distrito:str=None,codigoPostal:str=None,direccion:str=None,direccionSecundaria:str=None):
        self.__idLocalizacionComercio=idLocalizacionComercio if idLocalizacionComercio is not None else self.generaridLocalizacionComercio()

        self.oComercio=comercio
        Localizacion.__init__(self,provincia,distrito,codigoPostal,direccion,direccionSecundaria)

    @property
    def idLocalizacionComercio(self):
        return self.__idLocalizacionComercio

    @property
    def comercio(self):
        return self.oComercio
    @comercio.setter
    def comercio(self,newComercio):
        self.oComercio=newComercio


   
    def generaridLocalizacionComercio(self):
        count = 0
        database = sqlite3.connect("linioexp_parcial_lab3.db")  # ABRIR CONEXION CON BASE DE DATOS
        try:
            cursor = database.cursor()  # OBTENER OBJETO CURSOR
            query = '''
            SELECT COUNT(*) FROM localizacionComercio'''
            cursor.execute(query)
            count = cursor.fetchone()
        except Exception as e:
            print("Error: {}".format(e))
        finally:
            database.close()  # CERRAR CONEXION CON BASE DE DATOS

        return "LCOM" + "0" * (4 - len(str(count[0] + 1))) + str(count[0] + 1)
    def actualizarLocalizacion(self):
        database = sqlite3.connect("linioexp_parcial_lab3")
        cursor = database.cursor()
        query = '''
                    UPDATE localizacionComercio set provincia="{}",distrito="{}",  codigoPostal="{}",  direccion="{}",  direccionSecundaria="{}"
                    WHERE idLocalizacionComercio = '{}' 
                    '''.format(self.__provincia,self.__distrito, self.__codigoPostal, self.__direccion, self.__direccionSecundaria, self.idLocalizacionComercio)
        cursor.execute(query)
        database.commit()
        
    
    def agregarLocalizacion(self):
        database = sqlite3.connect("linioexp_parcial_lab3.db")  # ABRIR CONEXION CON BASE DE DATOS
        try:
            cursor = database.cursor()  # OBTENER OBJETO CURSOR

            query = '''INSERT INTO localizacionComercio(idLocalizacionComercio, provincia, distrito, codigoPostal, direccion, direccionSecundaria,idComercio)
                    VALUES ('{}','{}','{}','{}','{}','{}','{}')
                    '''.format(self.__idLocalizacionComercio,self.provincia,self.distrito,self.codigoPostal,self.direccion,self.direccionSecundaria,self.oComercio.idComercio)

            cursor.execute(query)
            database.commit()
        except Exception as e:
            print("Error: {}".format(e))
        finally:
            database.close()
    def obtenerLocalizacionComercio(self, id: str):
        pass
            
    

        

