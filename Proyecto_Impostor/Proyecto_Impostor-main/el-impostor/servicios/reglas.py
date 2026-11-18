import random
from abc import ABC, abstractmethod
from modelo.rol import Civil, Impostor


class IValidadorPista(ABC):
    @abstractmethod
    def validar_texto(self, texto):
        pass


class ValidadorLongitud(IValidadorPista):
    def __init__(self, minimo=3, maximo=20):
        self.minimo = minimo
        self.maximo = maximo

    def validar_texto(self, texto):
        return self.minimo <= len(texto.strip()) <= self.maximo


class ValidadorPalabraProhibida(IValidadorPista):
    def __init__(self, palabra_secreta):
        self.palabra_secreta = palabra_secreta

    def validar_texto(self, texto):
        return self.palabra_secreta.get_texto().lower() not in texto.lower()


class AsignadorRoles:
    def asignar(self, jugadores, palabra_secreta):
        impostor = random.choice(jugadores)
        for j in jugadores:
            j.set_rol(Impostor() if j is impostor else Civil(palabra_secreta))


class ContadorVotos:
    def contar(self, votos):
        conteo = {}
        for v in votos:
            conteo[v.get_acusado()] = conteo.get(v.get_acusado(), 0) + 1
        if not conteo:
            return None
        maximo = max(conteo.values())
        top = [j for j, n in conteo.items() if n == maximo]
        return top[0] if len(top) == 1 else None
