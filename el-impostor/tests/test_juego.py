import unittest
from modelo.jugador import Jugador, PalabraSecreta
from modelo.partida import Partida, Voto
from modelo.excepciones import (
    PistaInvalidaException, VotoInvalidoException, PartidaInvalidaException,
)
from servicios.reglas import (
    AsignadorRolesAleatorio, ContadorVotosMayoria, ValidadorLongitud, ValidadorPalabraProhibida,
)

def avanzar_a_votacion(ronda):
    ronda.avanzar_fase()  # PISTAS -> DEBATE
    ronda.avanzar_fase()  # DEBATE -> VOTACION


PALABRA = PalabraSecreta("manzana", "frutas")


def partida(n=3):
    js = [Jugador(i, f"J{i}") for i in range(n)]
    validadores = [ValidadorLongitud(), ValidadorPalabraProhibida(PALABRA)]
    return Partida(js, PALABRA, validadores, AsignadorRolesAleatorio(), ContadorVotosMayoria())


class TestJuego(unittest.TestCase):

    def test_un_solo_impostor(self):
        p = partida(5)
        p.iniciar()
        self.assertEqual(sum(j.get_rol().es_impostor() for j in p.get_jugadores()), 1)

    def test_validacion_de_pistas(self):
        p = partida()
        ronda = p.iniciar()
        j = p.get_jugadores()[0]
        for mala in ("A", "una manzana"):
            with self.assertRaises(PistaInvalidaException):
                ronda.registrar_pista(j.dar_pista(mala, 1))
        ronda.registrar_pista(j.dar_pista("roja", 1))
        self.assertEqual(len(ronda.get_pistas()), 1)

    def test_conteo_y_empate(self):
        a, b, c = partida().get_jugadores()
        self.assertIs(ContadorVotosMayoria().contar([Voto(a, b), Voto(c, b)]), b)
        self.assertIsNone(ContadorVotosMayoria().contar([Voto(a, b), Voto(b, c)]))
        self.assertIsNone(ContadorVotosMayoria().contar([]))

    def test_votos_invalidos(self):
        p = partida()
        ronda = p.iniciar()
        a, b, _ = p.get_jugadores()
        with self.assertRaises(VotoInvalidoException):
            a.votar(a)
        with self.assertRaises(VotoInvalidoException):
            ronda.registrar_voto(a.votar(b))
        avanzar_a_votacion(ronda)
        ronda.registrar_voto(a.votar(b))
        with self.assertRaises(VotoInvalidoException):
            ronda.registrar_voto(a.votar(b))

    def test_partida_invalida(self):
        with self.assertRaises(PartidaInvalidaException):
            partida(2)

    def test_ganan_civiles(self):
        p = partida()
        ronda = p.iniciar()
        avanzar_a_votacion(ronda)
        imp = next(j for j in p.get_jugadores() if j.get_rol().es_impostor())
        for j in p.get_jugadores():
            if j is not imp:
                ronda.registrar_voto(j.votar(imp))
        self.assertEqual(p.determinar_ganador(), "Civiles")

    def test_gana_impostor(self):
        p = partida()
        ronda = p.iniciar()
        avanzar_a_votacion(ronda)
        c1, c2 = [j for j in p.get_jugadores() if not j.get_rol().es_impostor()]
        ronda.registrar_voto(c2.votar(c1))
        self.assertEqual(p.determinar_ganador(), "Impostor")



class TestRegistroConsola(unittest.TestCase):
    def _vista(self, respuestas):
        from vista.vista_consola import VistaConsola
        respuestas = list(respuestas)
        return VistaConsola(entrada=lambda texto: respuestas.pop(0), salida=lambda t: None)

    def test_pide_la_cantidad_y_luego_solo_esos_nombres(self):
        vista = self._vista(["3", "Ana", "Beto", "Carla"])
        self.assertEqual(vista.pedir_jugadores(3, 10), ["Ana", "Beto", "Carla"])

    def test_cantidad_invalida_se_vuelve_a_pedir(self):
        vista = self._vista(["2", "abc", "11", "3", "Ana", "Beto", "Carla"])
        self.assertEqual(len(vista.pedir_jugadores(3, 10)), 3)

    def test_nombre_repetido_o_vacio_se_vuelve_a_pedir(self):
        vista = self._vista(["3", "Ana", "ana", "", "Beto", "Carla"])
        self.assertEqual(vista.pedir_jugadores(3, 10), ["Ana", "Beto", "Carla"])


if __name__ == "__main__":
    unittest.main()
