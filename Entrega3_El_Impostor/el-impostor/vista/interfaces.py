"""Interfaces pequeñas de la vista (ISP). El controlador solo depende de ellas (DIP)."""
from abc import ABC, abstractmethod


class IVistaJuego(ABC):
    @abstractmethod
    def mostrar_mensaje(self, texto):
        pass

    @abstractmethod
    def mostrar_error(self, texto):
        pass


class IVistaRegistro(IVistaJuego):
    @abstractmethod
    def pedir_jugadores(self, minimo, maximo):
        """Devuelve la lista de nombres escritos por el usuario."""

    @abstractmethod
    def pedir_configuracion(self, config, categorias):
        """Permite ajustar la configuración (RF-12) y la devuelve."""


class IVistaTurno(IVistaJuego):
    @abstractmethod
    def mostrar_rol_privado(self, nombre, rol, palabra_visible):
        pass

    @abstractmethod
    def pedir_pista(self, nombre, numero_turno):
        pass


class IVistaDebate(IVistaJuego):
    @abstractmethod
    def mostrar_debate(self, pistas, segundos):
        """pistas: lista de (nombre, texto)."""


class IVistaVotacion(IVistaJuego):
    @abstractmethod
    def pedir_voto(self, votante, candidatos):
        """Devuelve el nombre elegido entre candidatos."""

    @abstractmethod
    def pedir_adivinanza(self, nombre):
        pass


class IVistaResultado(IVistaJuego):
    @abstractmethod
    def mostrar_resultado(self, ganador, palabra, roles):
        """roles: lista de (nombre, rol, eliminado)."""

    @abstractmethod
    def mostrar_marcador(self, victorias):
        pass

    @abstractmethod
    def preguntar_otra_partida(self):
        pass
