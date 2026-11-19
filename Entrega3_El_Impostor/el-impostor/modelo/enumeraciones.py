from enum import Enum


class FaseJuego(Enum):
    """Fases por las que pasa una ronda."""
    REGISTRO = 1
    ASIGNACION = 2
    PISTAS = 3
    DEBATE = 4
    VOTACION = 5
    RESULTADO = 6
