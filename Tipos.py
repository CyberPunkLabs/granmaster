#! /user/bin/env python3


import random
import sys
import os
from models import Stockfish

sys.path.insert(1, "/home/diogenes/projects/granmaster/")

if os.name == 'nt':
    engine_path = "./engine/stockfish_20011801_x64.exe"
else: ### definir directorio propio !!
    engine_path = "/usr/games/stockfish"


parametros_tyrell = {"MultiPV": 4,
                     "Contempt": 0}
parametros_replicante = {"MultiPV": 4,
                         "Contempt": random.randint(-100, 100)}
    
    
def Tyrell(verbose=False):
    TYRELL = Stockfish(engine_path, parameters=parametros_tyrell)
    TYRELL.set_depth(20)
    TYRELL.set_skill_level(20)

    if verbose:
        ### Imprime parametros de Tyrell
        print("\n[CPLs] Parametros de Tyrell:")
        print(TYRELL.get_parameters())
    
    return TYRELL


def Replicante(habilidad, profundidad, verbose=False):
    REPLICANTE = Stockfish(engine_path, parameters=parametros_replicante)
    REPLICANTE.set_depth(profundidad)
    REPLICANTE.set_skill_level(habilidad)

    if verbose:        
        ### Imprime parametros de Replicante
        print("\n[CPLs] Parametros de Replicante:")
        print(REPLICANTE.get_parameters())

    return REPLICANTE

            

def JugadaHumano(Partida, REPLICANTE):
    entrada = Partida.imprimirPartida()
    #entrada = input().lower()
    #print("Jugada humano: {}".format(entrada))

    print("\nJugada humano")
    print("Jugada {} (movimiento {}; índice {})"\
          .format(Partida.n_jugada, Partida.n_movimiento+1,
                  Partida.n_movimiento))

    return entrada
    
        
def JugadaReplicante(entrada, Partida, REPLICANTE):
    print("\nVerificando jugada {}..."\
          .format(entrada))

    if (len(entrada) > 1) & (REPLICANTE.is_move_correct(entrada)):
        print("{} correcta !!".format(entrada))

        Partida.jugada_correcta = True
        # Añade la jugada a la lista
        Partida.variacion.append(entrada)
        # Suma un movimiento (ej 1. e2e5)
        Partida.n_movimiento += 1

        print("\nJugada Replicante")
        print("Jugada {} (movimiento {}; índice {})"\
              .format(Partida.n_jugada, Partida.n_movimiento+1,
                      Partida.n_movimiento))
        
        REPLICANTE.set_position(Partida.variacion)
        com = REPLICANTE.get_best_move()
        Partida.variacion.append(com)
        REPLICANTE.set_position(com)
        # Suma un movimiento (ej ... e7e5)
        Partida.n_movimiento += 1

    elif entrada == 'o':
        Partida.opciones(entrada)
        
    else:
        # Si la jugada no es correcta, lo desvia a la funcion "opciones"
        Partida.jugada_correcta = False
        lineas = ["{} Incorrecta !!".format(entrada)]
        Partida.imprimirGenerico(lineas, seleccion=False)
        time.sleep(3)


    # if Partida.jugada_correcta:


 
