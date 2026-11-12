from abc import ABC, abstractmethod

class Rol(ABC):
    def __init__(self, nombre: str):
        self.nombre = nombre

    @abstractmethod
    def conoce_palabra(self) -> bool:
        pass

class Civil(Rol):
    def __init__(self):
        super().__init__("Civil")

    def conoce_palabra(self) -> bool:
        return True  

class Impostor(Rol):
    def __init__(self):
        super().__init__("Impostor")

    def conoce_palabra(self) -> bool:
        return False 