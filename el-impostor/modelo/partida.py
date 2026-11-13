from enum import Enum


# ---------- Excepciones ----------
class PistaInvalidaException(Exception):
    pass


class VotoInvalidoException(Exception):
    pass


class PartidaInvalidaException(Exception):
    pass


# ---------- Fases ----------
class FaseJuego(Enum):
    REGISTRO = 1
    ASIGNACION = 2
    PISTAS = 3
    VOTACION = 4
    RESULTADO = 5


# ---------- Pista y Voto ----------
class Pista:
    def __init__(self, autor, texto, numero_turno):
        self.__autor = autor
        self.__texto = texto
        self.__numero_turno = numero_turno

    def get_autor(self):
        return self.__autor

    def get_texto(self):
        return self.__texto

    def get_numero_turno(self):
        return self.__numero_turno


class Voto:
    def __init__(self, votante, acusado):
        self.__votante = votante
        self.__acusado = acusado

    def get_votante(self):
        return self.__votante

    def get_acusado(self):
        return self.__acusado


# ---------- Ronda ----------
class Ronda:
    """Una ronda: primero pistas, luego votación."""

    def __init__(self, numero, validadores):
        self.__numero = numero
        self.__pistas = []
        self.__votos = []
        self.__fase = FaseJuego.PISTAS
        self.__validadores = validadores  # lista de IValidadorPista

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


# ---------- Partida ----------
class Partida:
    """Maneja jugadores, rondas y el resultado."""

    def __init__(self, jugadores, palabra, validadores, asignador, contador):
        nombres = [j.get_nombre() for j in jugadores]
        if not 3 <= len(jugadores) <= 10:
            raise PartidaInvalidaException("Deben ser entre 3 y 10 jugadores")
        if len(set(nombres)) != len(nombres):
            raise PartidaInvalidaException("Los nombres no se pueden repetir")
        self.__jugadores = jugadores
        self.__palabra = palabra
        self.__validadores = validadores
        self.__asignador = asignador  # se recibe por constructor
        self.__contador = contador
        self.__rondas = []

    def get_jugadores(self):
        return list(self.__jugadores)

    def get_rondas(self):
        return list(self.__rondas)

    def iniciar(self):
        self.__asignador.asignar(self.__jugadores, self.__palabra)
        self.nueva_ronda()

    def nueva_ronda(self):
        ronda = Ronda(len(self.__rondas) + 1, self.__validadores)
        self.__rondas.append(ronda)
        return ronda

    def determinar_ganador(self):
        """Devuelve 'Civiles', 'Impostor' o None si el juego sigue."""
        acusado = self.__contador.contar(self.__rondas[-1].get_votos())
        if acusado is not None and acusado.get_rol().es_impostor():
            return "Civiles"
        if acusado is not None:
            acusado.eliminar()  # acusaron a un inocente
        vivos = [j for j in self.__jugadores if not j.esta_eliminado()]
        if len(vivos) <= 2:
            return "Impostor"
        return None
