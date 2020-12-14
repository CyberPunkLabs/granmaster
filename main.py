#!/usr/bin/env python3

'''
[Pendientes]
-> Auditar la evaluacion de la jugada. Intentar actualizarla cada ej 3 s 
-> Traducir a ELO
-> Entrenador de aperturas
-> Que seleccione dificultad Stockfish segun ELO participante
-> Introducir scroll por partida
-> Introducir variantes
-> Cada perfil guarda todas las partidas, ELO, etc de un jugador
-> Numero de jugadas en nombre partida (para por ej reconocer las 
   partidas mas largas)
'''

# Modules
import sys
import random
import time
from matplotlib import pyplot

import Tipos
from models import Stockfish
from GranMaster import Partida

sys.path.insert(1, "/home/diogenes/projects/granmaster/")

TYRELL = Tipos.Tyrell()

### Crea  partida
Partida = Partida()
# Partida.menuInicio()


REPLICANTE = Tipos.Replicante(1, 12, verbose=True)

Partida.jugada_correcta = True
while True:
    time.sleep(1)
    print("\n##### Jugada nueva #####")
    entrada = Tipos.JugadaHumano(Partida, REPLICANTE)
    Tipos.JugadaReplicante(entrada, Partida, REPLICANTE)
    # Suma una jugada (ej 1. e2e4 e7e5)
    if Partida.jugada_correcta:
        Partida.n_jugada += 1

