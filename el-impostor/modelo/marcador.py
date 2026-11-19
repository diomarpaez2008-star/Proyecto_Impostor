class Marcador:
    """Marcador acumulado de partidas ganadas (RF-11)."""

    def __init__(self):
        self.victorias = {"Civiles": 0, "Impostor": 0}

    def registrar(self, ganador):
        self.victorias[ganador] += 1

    def get_victorias(self):
        return dict(self.victorias)
