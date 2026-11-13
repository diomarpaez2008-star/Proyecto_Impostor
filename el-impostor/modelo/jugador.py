from modelo.partida import Pista, Voto, VotoInvalidoException


class PalabraSecreta:
    """La palabra que los civiles conocen."""

    def __init__(self, texto, categoria):
        self.__texto = texto
        self.__categoria = categoria

    def get_texto(self):
        return self.__texto

    def get_categoria(self):
        return self.__categoria

    def coincide_con(self, texto):
        return self.__texto.strip().lower() == texto.strip().lower()


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
        if acusado is self:
            raise VotoInvalidoException("No puedes votar por ti mismo")
        if acusado.esta_eliminado():
            raise VotoInvalidoException("Ese jugador ya está eliminado")
        return Voto(self, acusado)
