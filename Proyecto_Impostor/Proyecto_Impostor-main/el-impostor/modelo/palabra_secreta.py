class PalabraSecreta:
    def __init__(self, texto, categoria):
        self.__texto = texto
        self.__categoria = categoria

    def get_texto(self):
        return self.__texto

    def get_categoria(self):
        return self.__categoria

    def coincide_con(self, texto):
        return self.__texto.strip().lower() == texto.strip().lower()
