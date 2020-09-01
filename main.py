#!/usr/bin/env python3

# Modules
from stockfish import Stockfish
from GranMaster import Partida

Partida    = Partida()
#Partida.crearPerfil()

Partida.depth = 4
Partida.skill = 10

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


def opciones(entrada):
    if entrada == "a":
        Partida.imprimirAnalisis()
    elif entrada == "t":
        print("[CPLs] Tablero:")
        Partida.tableroFEN()
        print("\n")
    elif entrada == "d":
        Partida.deshacer()
    elif entrada == "e":
        Partida.escribirPartida(tipo='juego')
    elif entrada == "p":
        REPLICANTE.set_position(Partida.variacion)
        print(REPLICANTE.get_board_visual())
    elif entrada in ["b", "n"]:
        Partida.posicionTablero(color=entrada)
    elif entrada == "l":
        Partida.leerPartida(tipo='juego')

    # Si la jugada es incorrecta (Motor.is_move_correct == False ??)
    else:
        print('''
                 -> (a)nalisis
                 -> (t)ablero
                 -> Posicion (f)EN
                 -> (d)eshacer
                 -> (e)scribir partida
                 -> (l)eer partida
                 -> posicion (b)lancas y (n)egras''')
        
    #self.titilar()
    Partida.jugada_correcta = False



tipo = 'blancas'
if tipo == 'blancas':
    reiniciar = False
    while not reiniciar:
        Partida.imprimirPartida()
        entrada = input().lower()

        if (len(entrada) > 1) & (REPLICANTE.is_move_correct(entrada)):
            Partida.jugada_correcta = True
            Partida.variacion.append(entrada)
            Partida.n_movimiento += 1

            if Partida.jugada_correcta:
                REPLICANTE.set_position(Partida.variacion)
                com = REPLICANTE.get_best_move()
                Partida.variacion.append(com)
                REPLICANTE.set_position(com)
                Partida.n_movimiento += 1
                Partida.n_jugada += 1

        else:
            Partida.jugada_correcta = False
            opciones(entrada)

        reiniciar = Partida.salir


    
#######################################
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


    
