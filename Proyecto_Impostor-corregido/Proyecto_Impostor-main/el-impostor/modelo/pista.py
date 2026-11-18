class Pista:
    def __init__(self, autor, texto, numero_turno):
        self.__autor = autor
        self.__texto = texto
        self.__numero_turno = numero_turno

    def get_autor(self):
        return self.__autor

    def get_texto(self):
        return self.__texto

    def get_numero_turno(self):
        return self.__numero_turno
