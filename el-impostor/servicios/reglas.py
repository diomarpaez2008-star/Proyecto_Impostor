import random
from abc import ABC, abstractmethod
from modelo.rol import Civil, Impostor


class IValidadorPista(ABC):
    """Interfaz pequeña: solo valida una pista."""

    @abstractmethod
    def validar_texto(self, texto):
        pass


class ValidadorLongitud(IValidadorPista):
    def __init__(self, maximo=20):
        self.__maximo = maximo

    def validar_texto(self, texto):
        return 0 < len(texto.strip()) <= self.__maximo


class ValidadorPalabraProhibida(IValidadorPista):
    def __init__(self, palabra_secreta):
        self.__palabra_secreta = palabra_secreta

    def validar_texto(self, texto):
        return self.__palabra_secreta.get_texto().lower() not in texto.lower()


class AsignadorRoles:
    """Escoge un impostor al azar; los demás son civiles."""

    def asignar(self, jugadores, palabra_secreta):
        impostor = random.choice(jugadores)
        for j in jugadores:
            if j is impostor:
                j.set_rol(Impostor())
            else:
                j.set_rol(Civil(palabra_secreta))


class ContadorVotos:
    """Gana el más votado. Si hay empate devuelve None."""

    def contar(self, votos):
        conteo = {}
        for v in votos:
            conteo[v.get_acusado()] = conteo.get(v.get_acusado(), 0) + 1
        if not conteo:
            return None
        maximo = max(conteo.values())
        ganadores = [j for j, n in conteo.items() if n == maximo]
        return ganadores[0] if len(ganadores) == 1 else None
