"""Raíz de composición: aquí se eligen las implementaciones concretas."""
import os
from controlador.controlador_partida import ControladorPartida
from modelo.configuracion import ConfiguracionPartida
from servicios.reglas import (
    AsignadorRolesAleatorio, ContadorVotosMayoria,
    ValidadorLongitud, ValidadorPalabraProhibida,
)
from servicios.repositorio_palabras import RepositorioPalabrasArchivo
from vista.vista_consola import VistaConsola


def fabrica_validadores(palabra, config):
    return [ValidadorLongitud(3, config.longitud_maxima_pista),
            ValidadorPalabraProhibida(palabra)]


def main():
    ruta = os.path.join(os.path.dirname(__file__), "datos", "palabras.json")
    ControladorPartida(
        VistaConsola(), RepositorioPalabrasArchivo(ruta),
        AsignadorRolesAleatorio(), ContadorVotosMayoria(),
        fabrica_validadores, ConfiguracionPartida(),
    ).jugar()


if __name__ == "__main__":
    main()
