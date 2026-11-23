from modelo.excepciones import PartidaInvalidaException
from modelo.jugador import Jugador
from modelo.marcador import Marcador
from modelo.partida import Partida
from controlador.controlador_ronda import ControladorRonda
from controlador.controlador_votacion import ControladorVotacion


class ControladorPartida:
    """Orquesta el flujo completo del juego.

    Todas sus dependencias llegan por constructor como abstracciones (DIP):
    vista, repositorio, asignador, contador y fábrica de validadores.
    """

    def __init__(self, vista, repositorio, asignador, contador,
                 fabrica_validadores, config):
        self.vista = vista
        self.repositorio = repositorio
        self.asignador = asignador
        self.contador = contador
        self.fabrica_validadores = fabrica_validadores
        self.config = config
        self.marcador = Marcador()

    def jugar(self):
        self.config = self.vista.pedir_configuracion(
            self.config, self.repositorio.categorias())
        while True:
            self.jugar_partida()
            self.vista.mostrar_marcador(self.marcador.get_victorias())
            if not self.vista.preguntar_otra_partida():
                break

    def jugar_partida(self):
        partida = self._crear_partida()
        ronda = partida.iniciar()
        self._mostrar_roles(partida)
        ganador = None
        while ganador is None:
            ControladorRonda(self.vista, partida, ronda,
                             self.config.segundos_debate).ejecutar()
            ganador = ControladorVotacion(
                self.vista, partida, ronda, self.config.ultima_oportunidad).ejecutar()
            if ganador is None:
                ronda = partida.nueva_ronda()
        self.marcador.registrar(ganador)
        roles = [(j.get_nombre(), j.get_rol().get_nombre(), j.esta_eliminado())
                 for j in partida.get_jugadores()]
        self.vista.mostrar_resultado(ganador, partida.get_palabra().get_texto(), roles)
        return ganador

    def _crear_partida(self):
        palabra = self.repositorio.obtener_aleatoria(self.config.categoria)
        validadores = self.fabrica_validadores(palabra, self.config)
        while True:
            nombres = self.vista.pedir_jugadores(3, 10)
            try:
                jugadores = [Jugador(i, n) for i, n in enumerate(nombres)]
                return Partida(jugadores, palabra, validadores, self.asignador,
                               self.contador, self.config.max_rondas)
            except PartidaInvalidaException as e:
                self.vista.mostrar_error(str(e))

    def _mostrar_roles(self, partida):
        for j in partida.get_jugadores():
            rol = j.get_rol()
            self.vista.mostrar_rol_privado(
                j.get_nombre(), rol.get_nombre(), rol.obtener_palabra_visible())
