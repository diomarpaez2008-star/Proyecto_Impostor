import unittest
from modelo.jugador import Jugador
from modelo.voto import Voto
from modelo.excepciones import PistaInvalidaException
from servicios.asignacion_roles import AsignadorRoles
from servicios.validacion_pistas import ValidadorLongitud
from servicios.conteo_votos import ContadorVotos

class TestJuego(unittest.TestCase):

    def test_asignacion_roles_garantiza_un_impostor(self):
        jugadores = [Jugador(1, "Ana"), Jugador(2, "Juan"), Jugador(3, "Pedro")]
        AsignadorRoles.asignar(jugadores)
        
        impostores = [j for j in jugadores if j.rol.nombre == "Impostor"]
        civiles = [j for j in jugadores if j.rol.nombre == "Civil"]
        
        self.assertEqual(len(impostores), 1)
        self.assertEqual(len(civiles), 2)

    def test_validacion_pista_lanza_excepcion_si_es_corta(self):
        validador = ValidadorLongitud(min_longitud=3)
        self.assertTrue(validador.validar("Rojo")) 
        
        with self.assertRaises(PistaInvalidaException):
            validador.validar("A") 

    def test_conteo_votos_elimina_al_mas_votado(self):
        j1 = Jugador(1, "Ana")
        j2 = Jugador(2, "Juan")
        j3 = Jugador(3, "Pedro")
        
      
        votos = [Voto(j1, j2), Voto(j3, j2)]
        
        eliminado = ContadorVotos.obtener_eliminado(votos)
        self.assertEqual(eliminado.nombre, "Juan")

if __name__ == '__main__':
    unittest.main()