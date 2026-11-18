import unittest
from modelo.jugador import Jugador
from modelo.voto import Voto
from modelo.palabra_secreta import PalabraSecreta
from modelo.partida import Partida
from modelo.excepciones import (
    PistaInvalidaException, VotoInvalidoException, PartidaInvalidaException,
)
from servicios.asignacion_roles import AsignadorRoles
from servicios.validacion_pistas import ValidadorLongitud, ValidadorPalabraProhibida
from servicios.conteo_votos import ContadorVotos

PALABRA = PalabraSecreta("manzana", "frutas")


def jugadores(n=3):
    return [Jugador(i, f"J{i}") for i in range(1, n + 1)]


def nueva_partida(js=None):
    js = js or jugadores()
    return Partida(js, PALABRA, [ValidadorLongitud(), ValidadorPalabraProhibida(PALABRA)],
                   AsignadorRoles(), ContadorVotos())


class TestJuego(unittest.TestCase):

    def test_asignacion_garantiza_un_impostor(self):
        js = jugadores(5)
        AsignadorRoles().asignar(js, PALABRA)
        self.assertEqual(sum(j.get_rol().es_impostor() for j in js), 1)
        civiles = [j for j in js if not j.get_rol().es_impostor()]
        self.assertTrue(all(c.get_rol().obtener_palabra_visible() == "manzana" for c in civiles))

    def test_impostor_no_conoce_palabra(self):
        js = jugadores()
        AsignadorRoles().asignar(js, PALABRA)
        imp = next(j for j in js if j.get_rol().es_impostor())
        self.assertFalse(imp.get_rol().conoce_palabra())

    def test_pista_corta_o_con_palabra_secreta_es_invalida(self):
        p = nueva_partida()
        ronda = p.iniciar()
        j = p.get_jugadores()[0]
        with self.assertRaises(PistaInvalidaException):
            ronda.registrar_pista(j.dar_pista("A", 1))
        with self.assertRaises(PistaInvalidaException):
            ronda.registrar_pista(j.dar_pista("una manzana", 1))
        ronda.registrar_pista(j.dar_pista("roja", 1))
        self.assertEqual(len(ronda.get_pistas()), 1)

    def test_conteo_elimina_al_mas_votado_y_empate_es_none(self):
        j1, j2, j3 = jugadores()
        c = ContadorVotos()
        self.assertIs(c.contar([Voto(j1, j2), Voto(j3, j2)]), j2)
        self.assertIsNone(c.contar([Voto(j1, j2), Voto(j2, j3)]))
        self.assertIsNone(c.contar([]))

    def test_no_puede_votarse_a_si_mismo(self):
        j1, j2, _ = jugadores()
        with self.assertRaises(VotoInvalidoException):
            j1.votar(j1)

    def test_voto_doble_y_fase_incorrecta(self):
        p = nueva_partida()
        ronda = p.iniciar()
        j1, j2, _ = p.get_jugadores()
        with self.assertRaises(VotoInvalidoException):
            ronda.registrar_voto(j1.votar(j2))  # aún en fase de pistas
        ronda.avanzar_fase()
        ronda.registrar_voto(j1.votar(j2))
        with self.assertRaises(VotoInvalidoException):
            ronda.registrar_voto(j1.votar(j2))

    def test_partida_valida_jugadores(self):
        with self.assertRaises(PartidaInvalidaException):
            nueva_partida(jugadores(2))
        with self.assertRaises(PartidaInvalidaException):
            nueva_partida([Jugador(1, "A"), Jugador(2, "A"), Jugador(3, "B")])

    def test_ganan_civiles_si_acusan_al_impostor(self):
        p = nueva_partida()
        ronda = p.iniciar()
        js = p.get_jugadores()
        imp = next(j for j in js if j.get_rol().es_impostor())
        ronda.avanzar_fase()
        for j in js:
            if j is not imp:
                ronda.registrar_voto(j.votar(imp))
        self.assertEqual(p.determinar_ganador(), "Civiles")

    def test_gana_impostor_si_quedan_dos_vivos(self):
        p = nueva_partida()
        ronda = p.iniciar()
        js = p.get_jugadores()
        civiles = [j for j in js if not j.get_rol().es_impostor()]
        ronda.avanzar_fase()
        ronda.registrar_voto(civiles[1].votar(civiles[0]))
        self.assertEqual(p.determinar_ganador(), "Impostor")


if __name__ == "__main__":
    unittest.main()
