from modelo.excepciones import PistaInvalidaException


class ControladorRonda:
    """Coordina las fases de pistas y debate de una ronda."""

    def __init__(self, vista, partida, ronda, segundos_debate):
        self.vista = vista
        self.partida = partida
        self.ronda = ronda
        self.segundos_debate = segundos_debate

    def ejecutar(self):
        self.vista.mostrar_mensaje(f"\n--- Ronda {self.ronda.get_numero()} ---")
        self._fase_pistas()
        self.ronda.avanzar_fase()  # PISTAS -> DEBATE
        self._fase_debate()
        self.ronda.avanzar_fase()  # DEBATE -> VOTACION

    def _fase_pistas(self):
        for turno, jugador in enumerate(self.partida.get_activos(), 1):
            while True:
                texto = self.vista.pedir_pista(jugador.get_nombre(), turno)
                try:
                    self.ronda.registrar_pista(jugador.dar_pista(texto, turno))
                    break
                except PistaInvalidaException as e:
                    self.vista.mostrar_error(str(e))

    def _fase_debate(self):
        pistas = [(p.get_autor().get_nombre(), p.get_texto())
                  for p in self.ronda.get_pistas()]
        self.vista.mostrar_debate(pistas, self.segundos_debate)
