import random
from modelo.rol import Civil, Impostor


class AsignadorRoles:
    """Escoge un impostor al azar; los demás son civiles."""

    def asignar(self, jugadores, palabra_secreta):
        if len(jugadores) < 3:
            raise ValueError("Se necesitan al menos 3 jugadores")
        impostor = random.choice(jugadores)
        for j in jugadores:
            j.set_rol(Impostor() if j is impostor else Civil(palabra_secreta))
