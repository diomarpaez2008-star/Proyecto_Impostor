from dataclasses import dataclass
from typing import Optional


@dataclass
class ConfiguracionPartida:
    """Parámetros configurables de la partida (RF-12)."""
    max_rondas: int = 3
    segundos_debate: int = 30
    categoria: Optional[str] = None
    ultima_oportunidad: bool = True
    longitud_maxima_pista: int = 20
