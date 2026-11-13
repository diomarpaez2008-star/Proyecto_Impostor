
class JuegoException(Exception):
    """Excepción base para el juego."""
    pass

class PistaInvalidaException(JuegoException):
    pass

class VotoInvalidoException(JuegoException):
    pass
