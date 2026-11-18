from modelo.ronda import Ronda
from modelo.excepciones import PartidaInvalidaException


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
        self.__asignador = asignador  # inyectado por constructor (DIP)
        self.__contador = contador
        self.__rondas = []

    def get_jugadores(self):
        return list(self.__jugadores)

    def get_rondas(self):
        return list(self.__rondas)

    def iniciar(self):
        self.__asignador.asignar(self.__jugadores, self.__palabra)
        return self.nueva_ronda()

    def nueva_ronda(self):
        ronda = Ronda(len(self.__rondas) + 1, self.__validadores)
        self.__rondas.append(ronda)
        return ronda

    def determinar_ganador(self):
        """Devuelve 'Civiles', 'Impostor' o None si el juego sigue."""
        if not self.__rondas:
            raise PartidaInvalidaException("La partida no ha iniciado")
        acusado = self.__contador.contar(self.__rondas[-1].get_votos())
        if acusado is not None and acusado.get_rol().es_impostor():
            return "Civiles"
        if acusado is not None:
            acusado.eliminar()  # acusaron a un inocente
        vivos = [j for j in self.__jugadores if not j.esta_eliminado()]
        if len(vivos) <= 2:
            return "Impostor"
        return None
