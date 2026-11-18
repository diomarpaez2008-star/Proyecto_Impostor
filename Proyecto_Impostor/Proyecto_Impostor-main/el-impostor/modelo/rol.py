from abc import ABC, abstractmethod


class Rol(ABC):
    def __init__(self, nombre):
        self.nombre = nombre

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
        self.palabra_secreta = palabra_secreta

    def conoce_palabra(self):
        return True

    def obtener_palabra_visible(self):
        return self.palabra_secreta.get_texto()


class Impostor(Rol):
    def __init__(self):
        super().__init__("Impostor")

    def conoce_palabra(self):
        return False

    def obtener_palabra_visible(self):
        return "???"

    def es_impostor(self):
        return True

    def puede_adivinar(self):
        return True

    def intenta_adivinar(self, palabra_secreta, texto):
        return palabra_secreta.coincide_con(texto)
