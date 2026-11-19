# El Impostor (POO - Python)

Juego de deducción hecho con POO, SOLID y MVC. Versión jugable por consola (Entrega 3).

## Estructura (MVC)
- `modelo/`: enumeraciones (FaseJuego), excepciones, Rol/Civil/Impostor, Jugador, PalabraSecreta, Partida, Ronda, Pista, Voto, Marcador, ConfiguracionPartida. No depende de vista ni controlador.
- `vista/`: interfaces pequeñas (IVistaRegistro, IVistaTurno, IVistaDebate, IVistaVotacion, IVistaResultado) y `VistaConsola`. Solo presenta y captura entrada.
- `controlador/`: `ControladorPartida`, `ControladorRonda`, `ControladorVotacion`. Reciben las abstracciones por constructor (inyección de dependencias).
- `servicios/`: validadores de pista, asignador de roles, contador de votos y repositorio de palabras (`datos/palabras.json`).
- `tests/`: pruebas unitarias del modelo, servicios y controladores (con una vista falsa).
- `docs/`: diagramas UML (`diagrama_uml.png`, `diagrama_mvc.png`, `diagrama_secuencia.png`; fuentes `.mmd`).
- `main.py`: raíz de composición (elige las implementaciones concretas).

## Ejecutar
```
python main.py
```
## Probar
```
python -m unittest discover -s tests -t .
```
Requiere Python 3.9+, sin dependencias externas.

## Integrantes
Diomar Páez y Cristopher Cabra
