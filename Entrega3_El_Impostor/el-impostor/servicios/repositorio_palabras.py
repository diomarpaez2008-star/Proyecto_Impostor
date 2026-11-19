import json
import random
from abc import ABC, abstractmethod
from modelo.jugador import PalabraSecreta


class IRepositorioPalabras(ABC):
    @abstractmethod
    def categorias(self):
        pass

    @abstractmethod
    def obtener_aleatoria(self, categoria=None):
        pass


class RepositorioPalabrasArchivo(IRepositorioPalabras):
    """Banco de palabras por categorías leído de un archivo JSON (RF-02)."""

    def __init__(self, ruta):
        with open(ruta, encoding="utf-8") as f:
            self._palabras = json.load(f)

    def categorias(self):
        return sorted(self._palabras)

    def obtener_aleatoria(self, categoria=None):
        if categoria is None:
            categoria = random.choice(self.categorias())
        if categoria not in self._palabras:
            raise KeyError("Categoría desconocida: " + categoria)
        return PalabraSecreta(random.choice(self._palabras[categoria]), categoria)
