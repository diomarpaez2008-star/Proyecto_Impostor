from abc import ABC, abstractmethod


class IValidadorPista(ABC):
    @abstractmethod
    def validar_texto(self, texto):
        pass


class ValidadorLongitud(IValidadorPista):
    def __init__(self, minimo=3, maximo=20):
        self.__minimo = minimo
        self.__maximo = maximo

    def validar_texto(self, texto):
        return self.__minimo <= len(texto.strip()) <= self.__maximo


class ValidadorPalabraProhibida(IValidadorPista):
    def __init__(self, palabra_secreta):
        self.__palabra_secreta = palabra_secreta

    def validar_texto(self, texto):
        return self.__palabra_secreta.get_texto().lower() not in texto.lower()
