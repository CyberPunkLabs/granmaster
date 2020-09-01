#!/usr/bin/env python3

# Modules
from stockfish import Stockfish
from GranMaster import Partida

Partida    = Partida()
Partida.crearPerfil()

print("Skill = {}".format(Partida.skill))
REPLICANTE = Stockfish("/usr/games/stockfish")
REPLICANTE.depth = Partida.depth
REPLICANTE.set_skill_level(Partida.skill)

TYRELL     = Stockfish("/usr/games/stockfish")
TYRELL.set_depth(15)
TYRELL.set_skill_level(20)

print('[CPLs] Parametros de REPLICANTE:')
print(REPLICANTE.get_parameters())
print('[CPLs] Parametros de TYRELL:')
print(TYRELL.get_parameters())


tipo = 'partida'
if tipo == 'partida':
    reiniciar = False
    while not reiniciar:
        Partida.imprimirPartida()
        entrada = input('Juega: ').lower()
        
        if (len(entrada) > 0) & REPLICANTE.is_move_correct(entrada):
            Partida.jugada_correcta = True
            Partida.variacion.append(entrada)
            Partida.n_movimiento += 1
            REPLICANTE.set_position(Partida.variacion)
            com = REPLICANTE.get_best_move()
            Partida.variacion.append(com)
            Partida.n_movimiento += 1
            Partida.n_jugada += 1

        else:
            Partida.manipularOpciones(entrada)
            #Partida.jugada_correcta = False
        

elif tipo == 'humano':
    variacion = Partida()
    reiniciar = False
    while not reiniciar:
        variacion.humano()

        reiniciar = variacion.salir
        #os.system('python3 main.py')

elif tipo == 'apertura':
    variacion = Partida()
    reiniciar = False
    while not reiniciar:
        variacion.apertura()

        reiniciar = variacion.salir
        #os.system('python3 main.py')


    
