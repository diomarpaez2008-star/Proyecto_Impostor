from abc import ABC, abstractmethod


class Rol(ABC):
    def __init__(self, nombre):
        self.__nombre = nombre

    @property
    def nombre(self):
        return self.__nombre

    @abstractmethod
    def conoce_palabra(self):
        pass

    @abstractmethod
    def obtener_palabra_visible(self):
        pass

    def es_impostor(self):
        return False


class Civil(Rol):
    def __init__(self, palabra_secreta):
        super().__init__("Civil")
        self.__palabra_secreta = palabra_secreta

    def conoce_palabra(self):
        return True

    def obtener_palabra_visible(self):
        return self.__palabra_secreta.get_texto()


class Impostor(Rol):
    def __init__(self):
        super().__init__("Impostor")

    def conoce_palabra(self):
        return False

    def obtener_palabra_visible(self):
        return "???"

    def es_impostor(self):
        return True
