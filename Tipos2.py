import random
import sys
import os
from models import Stockfish

sys.path.insert(1, "/home/diogenes/projects/granmaster/")


if os.name == 'nt':
    engine_path = "./engine/stockfish_20011801_x64.exe"
else: ### definir directorio propio !!
    engine_path = "/usr/games/stockfish"


class Tyrell:
    TYRELL = Stockfish(engine_path,
                       parameters={"MultiPV": 4, "Contempt": 0})
    TYRELL.set_depth(20)
    TYRELL.set_skill_level(20)

    ### Imprime parametros de Tyrell
    print("[CPLs] Parametros de Tyrell:")
    print(self.TYRELL.get_parameters())
    


class Replicante:

    REPLICANTE = Stockfish(engine_path, parameters={"MultiPV": 4, "Contempt": random.randint(-100, 100)})

    self.__init__(profundidad, habilidad):
        REPLICANTE.set_depth(parametros_replicante['profundidad'])
        REPLICANTE.set_skill_level(parametros_replicante['habilidad'])

        ### Imprime parametros de Replicante
        print("[CPLs] Parametros de Replicante:")
        print(self.REPLICANTE.get_parameters())

    def Jugada(self, Partida, entrada):
        if Partida.jugada_correcta:
            REPLICANTE.set_position(Partida.variacion)
            com = REPLICANTE.get_best_move()
            Partida.variacion.append(com)
            REPLICANTE.set_position(com)
            # Suma un movimiento (ej ... e7e5)
            Partida.n_movimiento += 1
            # Suma una jugada (ej 1. e2e4 e7e5)
            Partida.n_jugada += 1

        # Si la jugada no es correcta, lo desvia a la funcion "opciones"
        else:
            Partida.jugada_correcta = False
            Partida.opciones(entrada)

        #reiniciar = Partida.salir


            

def HUMANO(self, Partida, entrada):
    if (len(entrada) > 1) & (REPLICANTE.is_move_correct(entrada)):
        Partida.jugada_correcta = True
        # Añade la jugada a la lista
        Partida.variacion.append(entrada)
        # Suma un movimiento (ej 1. e2e5)
        Partida.n_movimiento += 1
        

