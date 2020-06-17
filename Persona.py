import datetime
class Persona(object):
    def __init__(self,nombre:str=None,apellidoPaterno:str=None,apellidoMaterno:str=None,dni:str=None,fechaNacimiento:datetime=None,genero:bool=None):
        self.__nombre=nombre
        self.__apellidoPaterno=apellidoPaterno
        self.__apellidoMaterno=apellidoMaterno
        self.__dni=dni
        self.__fechaNacimiento=fechaNacimiento
        self.__genero=genero #recien puesto editar
    @property
    def nombre(self):
        return self.__nombre
    @property
    def apellidoPaterno(self):
        return self.__apellidoPaterno
    @property
    def apellidoMaterno(self):
        return self.__apellidoMaterno
    @property
    def dni(self):
        return self.__dni
    @property
    def fechaNacimiento(self):
        return self.__fechaNacimiento
    @property
    def genero(self):
        return self.__genero
    @genero.setter
    def genero(self,newGenero:bool):
        self.__genero=newGenero
        
    @nombre.setter
    def nombre(self,newNombre):
        self.__nombre=newNombre
    @apellidoPaterno.setter
    def apellidoPaterno(self,newApellido):
        self.__apellidoPaterno=newApellido
    @apellidoMaterno.setter
    def apellidoMaterno(self, newApellido):
        self.__apellidoMaterno = newApellido
    @dni.setter
    def dni(self,newDni):
        self.__dni=newDni
    @fechaNacimiento.setter
    def fechaNacimiento(self,newfecha):
        self.__fechaNacimiento=newfecha
    
