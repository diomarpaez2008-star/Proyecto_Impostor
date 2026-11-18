class Voto:
    def __init__(self, votante, acusado):
        self.__votante = votante
        self.__acusado = acusado

    def get_votante(self):
        return self.__votante

    def get_acusado(self):
        return self.__acusado
