class ContadorVotos:
    """Gana el más votado. Si hay empate o no hay votos devuelve None."""

    def contar(self, votos):
        conteo = {}
        for v in votos:
            conteo[v.get_acusado()] = conteo.get(v.get_acusado(), 0) + 1
        if not conteo:
            return None
        maximo = max(conteo.values())
        mas_votados = [j for j, n in conteo.items() if n == maximo]
        return mas_votados[0] if len(mas_votados) == 1 else None
