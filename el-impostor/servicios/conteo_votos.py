from collections import Counter

class ContadorVotos
    @staticmethod
    def obtener_eliminado(votos)
        if not votos
            return None
        conteo = Counter(voto.acusado for voto in votos)
        return conteo.most_common(1)[0][0]