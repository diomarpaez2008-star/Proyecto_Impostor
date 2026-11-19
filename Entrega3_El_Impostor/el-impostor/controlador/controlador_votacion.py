from modelo.excepciones import VotoInvalidoException


class ControladorVotacion:
    """Coordina la votación y la resolución del resultado de la ronda."""

    def __init__(self, vista, partida, ronda, ultima_oportunidad):
        self.vista = vista
        self.partida = partida
        self.ronda = ronda
        self.ultima_oportunidad = ultima_oportunidad

    def ejecutar(self):
        """Devuelve "Civiles", "Impostor" o None si continúa el juego."""
        activos = self.partida.get_activos()
        for votante in activos:
            self._pedir_voto(votante, activos)
        self.ronda.avanzar_fase()  # VOTACION -> RESULTADO

        acusado = self.partida.acusado_de_la_ronda()
        intento = None
        if acusado is None:
            self.vista.mostrar_mensaje("Empate: nadie es eliminado.")
        elif self.partida.impostor_descubierto():
            self.vista.mostrar_mensaje(f"{acusado.get_nombre()} era el impostor.")
            if self.ultima_oportunidad:
                intento = self.vista.pedir_adivinanza(acusado.get_nombre())
        ganador = self.partida.determinar_ganador(intento)
        if acusado is not None and acusado.esta_eliminado():
            self.vista.mostrar_mensaje(
                f"{acusado.get_nombre()} era inocente y queda eliminado.")
        return ganador

    def _pedir_voto(self, votante, activos):
        candidatos = [j for j in activos if j is not votante]
        nombres = [j.get_nombre() for j in candidatos]
        while True:
            elegido = self.vista.pedir_voto(votante.get_nombre(), nombres)
            acusado = next((j for j in candidatos if j.get_nombre() == elegido), None)
            try:
                if acusado is None:
                    raise VotoInvalidoException("Jugador no válido")
                self.ronda.registrar_voto(votante.votar(acusado))
                return
            except VotoInvalidoException as e:
                self.vista.mostrar_error(str(e))
