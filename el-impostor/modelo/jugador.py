from modelo.partida import Pista, Voto
from modelo.excepciones import VotoInvalidoException


class PalabraSecreta:
    def __init__(self, texto, categoria):
        self.texto = texto
        self.categoria = categoria

    def get_texto(self):
        return self.texto

    def get_categoria(self):
        return self.categoria

    def coincide_con(self, texto):
        return self.texto.strip().lower() == texto.strip().lower()


class Jugador:
    def __init__(self, id, nombre):
        self.id = id
        self.nombre = nombre
        self.rol = None
        self.eliminado = False

    def get_id(self):
        return self.id

    def get_nombre(self):
        return self.nombre

    def get_rol(self):
        return self.rol

    def set_rol(self, rol):
        self.rol = rol

    def esta_eliminado(self):
        return self.eliminado

    def eliminar(self):
        self.eliminado = True

    def dar_pista(self, texto, numero_turno):
        return Pista(self, texto, numero_turno)

    def votar(self, acusado):
        if self.eliminado or acusado is self or acusado.eliminado:
            raise VotoInvalidoException("Voto no válido")
        return Voto(self, acusado)
