# El Impostor (POO - Python)

Juego de deducción hecho con POO, SOLID y MVC.

## Carpetas
- `modelo/`: enumeraciones, excepciones, rol, jugador (con PalabraSecreta), partida (con Pista, Voto, Ronda)
- `servicios/`: reglas.py (validadores de pistas, asignador de roles y contador de votos)
- `tests/`: pruebas unitarias
- `docs/`: diagrama UML

(La vista y el controlador se agregan en la Entrega 3.)

## Probar
```
python -m unittest discover -s tests -t .
```

## Integrantes
Diomar Páez y Cristopher Cabra
