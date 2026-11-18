from modelo.enumeraciones import FaseJuego
from modelo.excepciones import PistaInvalidaException, VotoInvalidoException


class Ronda:
    def __init__(self, numero, validadores):
        self.__numero = numero
        self.__pistas = []
        self.__votos = []
        self.__fase = FaseJuego.PISTAS
        self.__validadores = validadores

    def get_numero(self):
        return self.__numero

    def get_fase(self):
        return self.__fase

    def get_pistas(self):
        return list(self.__pistas)

    def get_votos(self):
        return list(self.__votos)

    def registrar_pista(self, pista):
        if self.__fase != FaseJuego.PISTAS:
            raise PistaInvalidaException("Ya no es fase de pistas")
        for v in self.__validadores:
            if not v.validar_texto(pista.get_texto()):
                raise PistaInvalidaException("Pista no válida: " + pista.get_texto())
        self.__pistas.append(pista)

    def registrar_voto(self, voto):
        if self.__fase != FaseJuego.VOTACION:
            raise VotoInvalidoException("Ya no es fase de votación")
        for otro in self.__votos:
            if otro.get_votante() is voto.get_votante():
                raise VotoInvalidoException("Este jugador ya votó")
        self.__votos.append(voto)

    def avanzar_fase(self):
        if self.__fase == FaseJuego.PISTAS:
            self.__fase = FaseJuego.VOTACION
        elif self.__fase == FaseJuego.VOTACION:
            self.__fase = FaseJuego.RESULTADO
