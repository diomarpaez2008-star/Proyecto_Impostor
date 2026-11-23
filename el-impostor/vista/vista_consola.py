import time
from vista.interfaces import (
    IVistaRegistro, IVistaTurno, IVistaDebate, IVistaVotacion, IVistaResultado,
)


class VistaConsola(IVistaRegistro, IVistaTurno, IVistaDebate,
                   IVistaVotacion, IVistaResultado):
    """Vista de consola: solo presenta datos y captura la entrada del usuario."""

    def __init__(self, entrada=input, salida=print, esperar=time.sleep):
        self._entrada = entrada
        self._salida = salida
        self._esperar = esperar

    # --- utilidades ---
    def _limpiar(self):
        self._salida("\n" * 40)

    def mostrar_mensaje(self, texto):
        self._salida(texto)

    def mostrar_error(self, texto):
        self._salida("[!] " + texto)

    # --- registro ---
    def pedir_jugadores(self, minimo, maximo):
        self._salida("=== EL IMPOSTOR ===")
        cantidad = self._pedir_cantidad(minimo, maximo)
        nombres = []
        while len(nombres) < cantidad:
            nombre = self._entrada(f"Nombre del jugador {len(nombres) + 1}: ").strip()
            if not nombre:
                self.mostrar_error("El nombre no puede estar vacío.")
            elif nombre.lower() in [n.lower() for n in nombres]:
                self.mostrar_error("Ese nombre ya está usado.")
            else:
                nombres.append(nombre)
        return nombres

    def _pedir_cantidad(self, minimo, maximo):
        while True:
            dato = self._entrada(f"¿Cuántos jugadores van a jugar? ({minimo}-{maximo}): ").strip()
            if dato.isdigit() and minimo <= int(dato) <= maximo:
                return int(dato)
            self.mostrar_error(f"Escribe un número entre {minimo} y {maximo}.")

    def pedir_configuracion(self, config, categorias):
        self._salida("Configuración (Enter para dejar el valor por defecto)")
        self._salida("Categorías: " + ", ".join(categorias))
        self._leer_entero(config, "max_rondas", "Número máximo de rondas")
        self._leer_entero(config, "segundos_debate", "Segundos de debate")
        cat = self._entrada(f"Categoría [{config.categoria or 'aleatoria'}]: ").strip()
        if cat in categorias:
            config.categoria = cat
        ult = self._entrada("¿Última oportunidad al impostor? (s/n) "
                            f"[{'s' if config.ultima_oportunidad else 'n'}]: ").strip().lower()
        if ult in ("s", "n"):
            config.ultima_oportunidad = ult == "s"
        return config

    def _leer_entero(self, config, atributo, texto):
        valor = self._entrada(f"{texto} [{getattr(config, atributo)}]: ").strip()
        if valor.isdigit() and int(valor) > 0:
            setattr(config, atributo, int(valor))

    # --- turnos ---
    def mostrar_rol_privado(self, nombre, rol, palabra_visible):
        self._limpiar()
        self._entrada(f"Turno de {nombre}. Que nadie más mire. Enter para ver tu rol...")
        self._salida(f"Rol: {rol}\nPalabra: {palabra_visible}")
        self._entrada("Enter para ocultar...")
        self._limpiar()

    def pedir_pista(self, nombre, numero_turno):
        return self._entrada(f"[Turno {numero_turno}] {nombre}, escribe tu pista: ")

    # --- debate ---
    def mostrar_debate(self, pistas, segundos):
        self._salida("\n=== DEBATE ===")
        for nombre, texto in pistas:
            self._salida(f"  {nombre}: {texto}")
        self._salida(f"Tienen {segundos} segundos para discutir...")
        self._esperar(segundos)

    # --- votación ---
    def pedir_voto(self, votante, candidatos):
        self._salida(f"\n{votante}, ¿quién es el impostor?")
        for i, c in enumerate(candidatos, 1):
            self._salida(f"  {i}) {c}")
        while True:
            op = self._entrada("Número o nombre: ").strip()
            if op.isdigit() and 1 <= int(op) <= len(candidatos):
                return candidatos[int(op) - 1]
            if op in candidatos:
                return op
            self.mostrar_error("Opción no válida.")

    def pedir_adivinanza(self, nombre):
        return self._entrada(f"{nombre}, te descubrieron. ¿Cuál es la palabra secreta? ")

    # --- resultado ---
    def mostrar_resultado(self, ganador, palabra, roles):
        self._salida(f"\n=== RESULTADO ===\nGanador: {ganador}\nPalabra: {palabra}")
        for nombre, rol, eliminado in roles:
            self._salida(f"  {nombre}: {rol}{' (eliminado)' if eliminado else ''}")

    def mostrar_marcador(self, victorias):
        self._salida("Marcador: " + " | ".join(f"{k}: {v}" for k, v in victorias.items()))

    def preguntar_otra_partida(self):
        return self._entrada("¿Jugar otra partida? (s/n): ").strip().lower() == "s"
