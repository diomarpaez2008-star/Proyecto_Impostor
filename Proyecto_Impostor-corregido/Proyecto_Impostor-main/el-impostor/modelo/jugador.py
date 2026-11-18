from modelo.pista import Pista
from modelo.voto import Voto
from modelo.excepciones import VotoInvalidoException


class Jugador:
    def __init__(self, id, nombre):
        self.__id = id
        self.__nombre = nombre
        self.__rol = None
        self.__eliminado = False

    def get_id(self):
        return self.__id

    def get_nombre(self):
        return self.__nombre

    def get_rol(self):
        return self.__rol

    def set_rol(self, rol):
        self.__rol = rol

    def esta_eliminado(self):
        return self.__eliminado

    def eliminar(self):
        self.__eliminado = True

    def dar_pista(self, texto, numero_turno):
        return Pista(self, texto, numero_turno)

    def votar(self, acusado):
        if self.__eliminado:
            raise VotoInvalidoException("Un jugador eliminado no puede votar")
        if acusado is self:
            raise VotoInvalidoException("No puedes votar por ti mismo")
        if acusado.esta_eliminado():
            raise VotoInvalidoException("Ese jugador ya está eliminado")
        return Voto(self, acusado)
