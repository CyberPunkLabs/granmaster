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
from models import Stockfish
from GranMaster import Partida
import random

### Crea  partida
Partida = Partida()
# Imprime pantalla para crear perfiles o cargar una nueva partida
Partida.crearPerfil()

# Define la arrogancia del Replicante. -100 implica un juego mas
# bien timido y defensivo, mientras +100 implica un juego mas
# arriesgado y temerario. El nivel de arrogancia de los Replicantes
# es una caracteristica que aleatoria que el humano no puede manipular.
arrogancia = random.randint(-100, 100)

### Crea un Replicante
REPLICANTE = Stockfish(parameters={"Contempt": arrogancia, "MultiPV": 1})
# Fija profundidad y habilidad segun eleccion del humano,
# (cuando no es una perfil cargado)
REPLICANTE.set_depth(Partida.profundidad_analisis)
REPLICANTE.set_skill_level(Partida.habilidad)

# Para desarrolladores
print('[CPLs] Parametros de REPLICANTE:')
print(REPLICANTE.get_parameters())

### Maneja las opciones del juego
def opciones(entrada):
    # Imprime el analisis de Tyrell (Stockfish depth:15, skill:20, PV:4)
    if entrada == "a":
        Partida.imprimirAnalisis()
    # Imprime el tablero en lindas figuras Unicode
    elif entrada == "t":
        print("[CPLs] Tablero:")
        Partida.imprimirTablero()
        print("\n")
    # Deshace la jugada
    elif entrada == "d":
        Partida.deshacer()
    # Escribe la partida en un perfil de usuario
    elif entrada == "e":
        Partida.escribirPartida(tipo='juego')
    # Imprime el tablero en letras (desarrolladores)
    elif entrada == "p":
        REPLICANTE.set_position(Partida.variacion)
        print(REPLICANTE.get_board_visual())
    # Imprime la posicion de las blancas o negras
    elif entrada in ["b", "n"]:
        Partida.posicionTablero(color=entrada)
    # Lee la partida un un perfil guardado
    elif entrada == "l":
        Partida.leerPartida(tipo='juego')

    # Ante una opcion incorrecta:
    else:
        print('''
                 -> (a)nalisis
                 -> (t)ablero
                 -> Posicion (f)EN
                 -> (d)eshacer
                 -> (e)scribir partida
                 -> (l)eer partida
                 -> posicion (b)lancas y (n)egras''')

    # Con LCD, hace titilar la pantalla
    #self.titilar()
    Partida.jugada_correcta = False


### Define tipo de partida, entre:
### blancas: Humano - Replicante
### negras: Replicante - Humano
### humano: Humano - Humano
### replicante: Replicante - Replicante
### apertura: Humano - Libro de aperturas (Modern Chess Openings - de Firmian)
### tutor: Humano - My System (My System - Nimwitich)
### leyendas: Humano - Partidas legendarias 
tipo = 'blancas'
if tipo == 'blancas':
    reiniciar = False
    while not reiniciar:
        # Ordena la informacion relevante sobre la partida
        # y la formatea para imprimirla en la LCD 84x48
        Partida.imprimirPartida()
        # Espera y registra la jugada de humano
        entrada = input().lower()

        # Si la jugada es correcta:
        if (len(entrada) > 1) & (REPLICANTE.is_move_correct(entrada)):
            Partida.jugada_correcta = True
            # Añade la jugada a la lista
            Partida.variacion.append(entrada)
            # Suma un movimiento (ej 1. e2e5)
            Partida.n_movimiento += 1

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
            opciones(entrada)

        reiniciar = Partida.salir


    
#######################################
### Template para Humano - Humano
elif tipo == 'humano':
    variacion = Partida()
    reiniciar = False
    while not reiniciar:
        variacion.humano()

        reiniciar = variacion.salir
        #os.system('python3 main.py')

### Template para Humano - Libro de aperturas
elif tipo == 'apertura':
    variacion = Partida()
    reiniciar = False
    while not reiniciar:
        variacion.apertura()

        reiniciar = variacion.salir
        #os.system('python3 main.py')

### Etc

    
