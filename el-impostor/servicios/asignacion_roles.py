import random
from modelo.rol import Civil, Impostor

class AsignadorRoles:
    @staticmethod
    def asignar(jugadores):
        if not jugadores or len(jugadores) < 3:
            raise Exception("Se necesitan al menos 3 jugadores.")
        
        impostor = random.choice(jugadores)
        for jugador in jugadores:
            if jugador == impostor:
                jugador.rol = Impostor()
            else:
                jugador.rol = Civil()