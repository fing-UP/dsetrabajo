import sqlite3
class Localizacion(object):
    def __init__(self,provincia:str=None,distrito:str=None,codigoPostal:str=None,direccion:str=None,direccionSecundaria:str=None):
        self.__provincia=provincia
        self.__distrito=distrito
        self.__codigoPostal=codigoPostal
        self.__direccion=direccion
        self.__direccionSecundaria=direccionSecundaria
    @property
    def provincia(self):
        return self.__provincia
    @property
    def distrito(self):
        return self.__distrito
    @property
    def codigoPostal(self):
        return self.__codigoPostal
    @property
    def direccion(self):
        return self.__direccion
    @property
    def direccionSecundaria(self):
        return self.__direccionSecundaria
    
    @provincia.setter
    def provincia(self,newProvincia):
        self.__provincia=newProvincia
    @distrito.setter
    def distrito(self,newDistrito):
        self.__distrito=newDistrito
    @codigoPostal.setter
    def codigoPostal(self,newCodigo):
        self.__codigoPostal=newCodigo
    @direccion.setter
    def direccion(self,newDireccion):
        self.__direccion=newDireccion
    @direccionSecundaria.setter
    def direccionSecundaria(self,newDireccion):
        self.__direccionSecundaria=newDireccion

    
    

