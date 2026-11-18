class JuegoException(Exception):
    """Excepción base para el juego."""


class PistaInvalidaException(JuegoException):
    pass


class VotoInvalidoException(JuegoException):
    pass


class PartidaInvalidaException(JuegoException):
    pass
