import os
import tempfile
import unittest
import json

from controlador.controlador_partida import ControladorPartida
from modelo.configuracion import ConfiguracionPartida
from modelo.rol import Civil, Impostor
from servicios.reglas import (
    ContadorVotosMayoria, IAsignadorRoles, ValidadorLongitud, ValidadorPalabraProhibida,
)
from servicios.repositorio_palabras import IRepositorioPalabras, RepositorioPalabrasArchivo
from modelo.jugador import PalabraSecreta
from vista.interfaces import (
    IVistaRegistro, IVistaTurno, IVistaDebate, IVistaVotacion, IVistaResultado,
)


class AsignadorFijo(IAsignadorRoles):
    """El primer jugador siempre es el impostor (determinista)."""

    def asignar(self, jugadores, palabra):
        for i, j in enumerate(jugadores):
            j.set_rol(Impostor() if i == 0 else Civil(palabra))


class RepoFijo(IRepositorioPalabras):
    def categorias(self):
        return ["lugares"]

    def obtener_aleatoria(self, categoria=None):
        return PalabraSecreta("playa", "lugares")


class VistaFalsa(IVistaRegistro, IVistaTurno, IVistaDebate, IVistaVotacion, IVistaResultado):
    """Vista guionada: no imprime nada, devuelve respuestas predefinidas."""

    def __init__(self, nombres, pistas, votos, adivinanza="x", otra=False):
        self.nombres, self.pistas, self.votos = nombres, list(pistas), list(votos)
        self.adivinanza, self.otra = adivinanza, otra
        self.errores, self.mensajes, self.resultados = [], [], []
        self.roles_vistos, self.debates = [], []

    def mostrar_mensaje(self, t): self.mensajes.append(t)
    def mostrar_error(self, t): self.errores.append(t)
    def pedir_jugadores(self, mn, mx): return self.nombres
    def pedir_configuracion(self, c, cats): return c
    def mostrar_rol_privado(self, n, r, p): self.roles_vistos.append((n, r, p))
    def pedir_pista(self, n, t): return self.pistas.pop(0)
    def mostrar_debate(self, pistas, s): self.debates.append(pistas)
    def pedir_voto(self, v, cands): return self.votos.pop(0)
    def pedir_adivinanza(self, n): return self.adivinanza
    def mostrar_resultado(self, g, p, r): self.resultados.append((g, p, r))
    def mostrar_marcador(self, v): self.marcador = v
    def preguntar_otra_partida(self): return self.otra


def fabrica(palabra, config):
    return [ValidadorLongitud(3, config.longitud_maxima_pista), ValidadorPalabraProhibida(palabra)]


def controlador(vista, **cfg):
    return ControladorPartida(vista, RepoFijo(), AsignadorFijo(), ContadorVotosMayoria(),
                              fabrica, ConfiguracionPartida(segundos_debate=0, **cfg))


NOMBRES = ["Ana", "Beto", "Caro"]  # Ana es impostora


class TestControladores(unittest.TestCase):

    def test_civiles_ganan_si_descubren_y_impostor_falla(self):
        v = VistaFalsa(NOMBRES, ["hola1", "arena", "sol"], ["Beto", "Ana", "Ana"], "mar")
        c = controlador(v)
        self.assertEqual(c.jugar_partida(), "Civiles")
        self.assertEqual(c.marcador.get_victorias(), {"Civiles": 1, "Impostor": 0})
        self.assertEqual(v.resultados[0][1], "playa")

    def test_ultima_oportunidad_acierta(self):
        v = VistaFalsa(NOMBRES, ["hola1", "arena", "sol"], ["Beto", "Ana", "Ana"], "PLAYA")
        self.assertEqual(controlador(v).jugar_partida(), "Impostor")

    def test_ultima_oportunidad_desactivada(self):
        v = VistaFalsa(NOMBRES, ["hola1", "arena", "sol"], ["Beto", "Ana", "Ana"], "playa")
        self.assertEqual(controlador(v, ultima_oportunidad=False).jugar_partida(), "Civiles")

    def test_roles_privados_solo_civil_ve_palabra(self):
        v = VistaFalsa(NOMBRES, ["hola1", "arena", "sol"], ["Beto", "Ana", "Ana"])
        controlador(v).jugar_partida()
        self.assertEqual(v.roles_vistos[0], ("Ana", "Impostor", "???"))
        self.assertEqual(v.roles_vistos[1], ("Beto", "Civil", "playa"))

    def test_pista_invalida_se_vuelve_a_pedir(self):
        v = VistaFalsa(NOMBRES, ["la playa", "hola1", "arena", "sol"], ["Beto", "Ana", "Ana"])
        controlador(v).jugar_partida()
        self.assertEqual(len(v.errores), 1)

    def test_voto_a_si_mismo_se_rechaza(self):
        v = VistaFalsa(NOMBRES, ["hola1", "arena", "sol"], ["Ana", "Beto", "Ana", "Ana"])
        controlador(v).jugar_partida()
        self.assertEqual(len(v.errores), 1)

    def test_inocente_eliminado_con_cuatro_jugadores_continua(self):
        nombres = ["Ana", "Beto", "Caro", "Dani"]
        pistas = ["hola1", "arena", "sol", "mar",   # ronda 1
                  "hola2", "olas", "viaje"]          # ronda 2 (sin Beto)
        votos = ["Beto", "Caro", "Beto", "Beto",     # ronda 1: elimina a Beto
                 "Caro", "Ana", "Ana"]               # ronda 2: descubren a Ana
        v = VistaFalsa(nombres, pistas, votos, "no")
        self.assertEqual(controlador(v).jugar_partida(), "Civiles")
        self.assertEqual(len(v.debates), 2)
        self.assertEqual(len(v.debates[1]), 3)

    def test_empate_sin_eliminados_y_limite_de_rondas(self):
        nombres = ["Ana", "Beto", "Caro", "Dani"]
        pistas = ["hola1", "arena", "sol", "mar"] * 2
        votos = ["Beto", "Ana", "Beto", "Ana"] * 2   # 2-2 siempre
        v = VistaFalsa(nombres, pistas, votos)
        self.assertEqual(controlador(v, max_rondas=2).jugar_partida(), "Impostor")

    def test_jugar_acumula_marcador(self):
        v = VistaFalsa(NOMBRES, ["hola1", "arena", "sol"] * 2,
                       ["Beto", "Ana", "Ana"] * 2, "no")
        c = controlador(v)
        respuestas = iter([True, False])
        v.preguntar_otra_partida = lambda: next(respuestas)
        c.jugar()
        self.assertEqual(c.marcador.get_victorias()["Civiles"], 2)


class TestRepositorio(unittest.TestCase):
    def test_lee_categorias_y_palabra(self):
        with tempfile.TemporaryDirectory() as d:
            ruta = os.path.join(d, "p.json")
            with open(ruta, "w", encoding="utf-8") as f:
                json.dump({"a": ["uno"], "b": ["dos"]}, f)
            repo = RepositorioPalabrasArchivo(ruta)
            self.assertEqual(repo.categorias(), ["a", "b"])
            self.assertEqual(repo.obtener_aleatoria("b").get_texto(), "dos")
            with self.assertRaises(KeyError):
                repo.obtener_aleatoria("zzz")


if __name__ == "__main__":
    unittest.main()
