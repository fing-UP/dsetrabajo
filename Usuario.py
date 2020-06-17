from Persona import Persona
import sqlite3
import datetime as datetime

class Usuario(Persona):
    def __init__(self, nombre:str=None,apellidoPaterno:str=None,apellidoMaterno:str=None,dni:str=None,fechaNacimiento:datetime=None, correo: str = None, nombreusuario: str = None, password: str = None, fechaRegistro: datetime = None,genero:bool=None):
        self.__correo=correo
        self.__nombreUsuario=nombreusuario
        self.__password=password
        self.__fechaRegistro=fechaRegistro
        #self.__oPersona=Persona()
        Persona.__init__(self, nombre, apellidoPaterno, apellidoMaterno, dni, fechaNacimiento,genero)

    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, new_correo):
        self.__correo = new_correo

    @property
    def nombreUsuario(self):
        return self.__nombreUsuario

    @nombreUsuario.setter
    def nombreUsuario(self, new_nombreUsuario):
        self.__nombreUsuario = new_nombreUsuario

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, new_password):
        self.__password = new_password

    @property
    def fechaRegistro(self):
        return self.__fechaRegistro

    @fechaRegistro.setter
    def fechaRegistro(self, new_fechaRegistro):
        self.__fechaRegistro = new_fechaRegistro
    '''@property
    def oPersona(self):
        return self.__oPersona

    @oPersona.setter
    def oPersona(self, pPersona):
        self.__oPersona = pPersona'''


   