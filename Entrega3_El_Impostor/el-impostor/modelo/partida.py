from modelo.enumeraciones import FaseJuego
from modelo.excepciones import (
    PistaInvalidaException, VotoInvalidoException, PartidaInvalidaException,
)


class Pista:
    def __init__(self, autor, texto, numero_turno):
        self.autor = autor
        self.texto = texto
        self.numero_turno = numero_turno

    def get_autor(self):
        return self.autor

    def get_texto(self):
        return self.texto

    def get_numero_turno(self):
        return self.numero_turno


class Voto:
    def __init__(self, votante, acusado):
        self.votante = votante
        self.acusado = acusado

    def get_votante(self):
        return self.votante

    def get_acusado(self):
        return self.acusado


class Ronda:
    def __init__(self, numero, validadores):
        self.numero = numero
        self.validadores = validadores
        self.pistas = []
        self.votos = []
        self.fase = FaseJuego.PISTAS

    def get_numero(self):
        return self.numero

    def get_fase(self):
        return self.fase

    def get_pistas(self):
        return list(self.pistas)

    def get_votos(self):
        return list(self.votos)

    def registrar_pista(self, pista):
        if self.fase != FaseJuego.PISTAS:
            raise PistaInvalidaException("Ya no es fase de pistas")
        if not all(v.validar_texto(pista.get_texto()) for v in self.validadores):
            raise PistaInvalidaException("Pista no válida: " + pista.get_texto())
        self.pistas.append(pista)

    def registrar_voto(self, voto):
        if self.fase != FaseJuego.VOTACION:
            raise VotoInvalidoException("Ya no es fase de votación")
        if any(v.get_votante() is voto.get_votante() for v in self.votos):
            raise VotoInvalidoException("Este jugador ya votó")
        self.votos.append(voto)

    def avanzar_fase(self):
        if self.fase == FaseJuego.PISTAS:
            self.fase = FaseJuego.DEBATE
        elif self.fase == FaseJuego.DEBATE:
            self.fase = FaseJuego.VOTACION
        elif self.fase == FaseJuego.VOTACION:
            self.fase = FaseJuego.RESULTADO


class Partida:
    """Agregado raíz: coordina jugadores, rondas y el resultado.

    Recibe por constructor las abstracciones de asignación y conteo (DIP).
    """

    def __init__(self, jugadores, palabra, validadores, asignador, contador,
                 max_rondas=None):
        nombres = [j.get_nombre() for j in jugadores]
        if not 3 <= len(jugadores) <= 10:
            raise PartidaInvalidaException("Deben ser entre 3 y 10 jugadores")
        if len(set(nombres)) != len(nombres):
            raise PartidaInvalidaException("Los nombres no se pueden repetir")
        self.jugadores = jugadores
        self.palabra = palabra
        self.validadores = validadores
        self.asignador = asignador
        self.contador = contador
        self.max_rondas = max_rondas
        self.rondas = []

    def get_jugadores(self):
        return list(self.jugadores)

    def get_activos(self):
        return [j for j in self.jugadores if not j.esta_eliminado()]

    def get_rondas(self):
        return list(self.rondas)

    def get_palabra(self):
        return self.palabra

    def iniciar(self):
        self.asignador.asignar(self.jugadores, self.palabra)
        return self.nueva_ronda()

    def nueva_ronda(self):
        ronda = Ronda(len(self.rondas) + 1, self.validadores)
        self.rondas.append(ronda)
        return ronda

    def acusado_de_la_ronda(self):
        """Jugador más votado de la última ronda (None si hay empate o no hay votos)."""
        return self.contador.contar(self.rondas[-1].get_votos())

    def impostor_descubierto(self):
        acusado = self.acusado_de_la_ronda()
        return acusado is not None and acusado.get_rol().es_impostor()

    def determinar_ganador(self, intento_impostor=None):
        """Devuelve "Civiles", "Impostor" o None si el juego continúa.

        Si el impostor es descubierto puede ganar adivinando la palabra.
        Si se acusa a un inocente, este queda eliminado.
        """
        acusado = self.acusado_de_la_ronda()
        if acusado is not None and acusado.get_rol().es_impostor():
            if intento_impostor and acusado.get_rol().intenta_adivinar(
                    self.palabra, intento_impostor):
                return "Impostor"
            return "Civiles"
        if acusado is not None:
            acusado.eliminar()
        if len(self.get_activos()) <= 2:
            return "Impostor"
        if self.max_rondas is not None and len(self.rondas) >= self.max_rondas:
            return "Impostor"
        return None
