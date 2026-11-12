from abc import ABC, abstractmethod
from modelo.excepciones import PistaInvalidaException

class IValidadorPista(ABC):
    @abstractmethod
    def validar(self, texto: str) -> bool:
        pass

class ValidadorLongitud(IValidadorPista):
    def __init__(self, min_longitud=3):
        self.min_longitud = min_longitud

    def validar(self, texto: str) -> bool:
        if len(texto.strip()) < self.min_longitud:
            raise PistaInvalidaException(f"La pista debe tener al menos {self.min_longitud} letras.")
        return True