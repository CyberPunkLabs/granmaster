### Importa modulos requieridos por Gran Master
#import os
import glob
import time
import pickle
import random
import numpy as np
from datetime import datetime
#from lcd5110 import LCD5110
from models import Stockfish

### Crea a Tyrell, como instancia de Stockfish
TYRELL = Stockfish("/usr/games/stockfish", parameters={"MultiPV": 4, "Contempt": 0})
TYRELL.set_depth(20)
TYRELL.set_skill_level(20)

### Imprime parametros de Tyrell
print("[CPLs] Parametros de Tyrell:")
print(TYRELL.get_parameters())
#lcd = LCD5110()


### Clase principal
class Partida:

    ''' Llama a stockfish y efectua e imprime la jugada.

[Historial]
20200825 -> Introduce funcionalidad de analisis modificando script de stockfish
         -> Script de stockfish queda almacenado en la misma carpeta de GranMaster


[Pendientes]
-> Auditar la evaluacion de la jugada. Intentar actualizarla cada ej 3 s 
-> Traducir a ELO
-> Entrenador de aperturas
-> Que seleccione dificultad Stockfish segun ELO participante
-> Introducir scroll por partida
-> Introducir variantes
-> Cada perfil guarda todas las partidas, ELO, etc de un jugador
-> Numero de jugada en nombre partida
'''


    ### Declara variables basicas
    aperturas = pickle.load(open('basesdatos/libroAperturas.gm', 'rb'))
    diccionario_unicode = pickle.load(open('basesdatos/piezas.unicode', 'rb'))
    variacion = []
    n_movimiento = 0
    n_jugada = 1
    jugada_correcta = True
    salir = False
    imprimir_tablero = False
    verbose = False
    #lcd_on = True


    ### Pantalla de inicio. Revisar si adecuado declararla en __init__
    def __init__(self):
        ### Despliega pantallas de configuracion
        #self.crearPerfil()
        self.contempt = 0
        self.color = 'blancas'
        self.perfil = "prueba"

        if self.color == 'blancas':
            jugador_blancas = self.perfil,
            jugador_negras = 'Replicante' #{}.{}'.format(self.depth, self.skill),
        else:
            jugador_negras = self.perfil,
            jugador_blancas = 'Replicante' #{}.{}'.format(self.depth, self.skill),

        ### Construye header con info sobre la partida (por implementar)
        now = datetime.now()
        self.header = dict(
                      evento          = 'Testeos GranMaster',
                      lugar           = 'Laboratorios CyberPunk',
                      fecha           = now.strftime("%d/%m/%Y_%H:%M:%S"),
                      ronda           = 1,
                      jugador_blancas = jugador_blancas,
                      jugador_negras  = jugador_negras,
                      resultado       = '*/*')



##################               FUNCIONES              #####################

    ### Define libro de apertura
    def LIBRO(self, entrada):
        if entrada == Partida.apertura[Partida.n_movimiento]:
            self.imprimirGenerico('Jugando', 'apertura...', dwell=1)

            ### Toma jugada desde libro de aperturas
            com = Partida.apertura[Partida.n_movimiento]

	    ### Agrega la jugada al arbol de la partida
            Partida.variacion.append(com)
            Partida.n_movimiento += 1

            self.evaluarPosicion()
            #self.imprimirNegras()

        ### Si la jugada no es correcta, simplementa pasa
        else:
            pass


    ### Imprimir analisis
    def imprimirAnalisis(self):
        TYRELL.set_position(Partida.variacion)
        analisis = TYRELL.get_analysis()

        info = []
        for linea in analisis:
            splitted_line = linea.split(" ")
            if splitted_line[0] == "info":
                info.append(splitted_line)

        info = info[-4:]
        evaluacion = []
        variacion = []
        for linea in info:
            for palabra in range(len(linea)):
                if linea[palabra] == "cp":
                    temp = np.float(linea[palabra+1]) / 100
                    if self.color == 'negras':
                        temp = temp * -1
                    if temp >= 0:
                        evaluacion.append("+{}".format(temp))
                    else:
                        evaluacion.append("{}".format(temp))
                if linea[palabra] == "pv":

                    variacion.append(linea[palabra+1:])
        self.imprimirGenerico("[Análisis]",
                              "{} {}".format(evaluacion[0], variacion[0]),
                              "{} {}".format(evaluacion[1], variacion[1]),
                              "{} {}".format(evaluacion[2], variacion[2]),
                              "{} {}".format(evaluacion[3], variacion[3]),
                              dwell=2)
        print("\n")


    ### Deshacer jugada
    def deshacer(self):
        Partida.jugada_correcta = False

        ### Si la partida tiene mas de 1 movimiento:
        if len(Partida.variacion) > 2:
            # Borra las ultimas dos
            del Partida.variacion[-2:]

            Partida.n_jugada     -= 1
            Partida.n_movimiento -= 2

        # Si no hay jugadas suficientes para deshacer
        else:
            self.imprimirGenerico("No hay mas jugadas", "que deshacer!", dwell=2)

        self.imprimirPartida()


    ### Imprimir pantalla para negras
    def imprimirPartida(self):
        self.formatearPartida()

        if self.color == 'blancas':
            if Partida.n_jugada == 1:
                line2 = " 1. {} {}".format(Partida.ultimas[0], Partida.ultimas[1])
                line3 = " 2. {} {}".format(Partida.ultimas[2], Partida.ultimas[3])
                Partida.evaluacion = " "
            elif Partida.n_jugada == 2:
                line2 = " 1. {} {}".format(Partida.ultimas[0], Partida.ultimas[1])
                line3 = " 2. {} {}".format(Partida.ultimas[2], Partida.ultimas[3])
            else:
                line2 = " {}. {} {}".format(Partida.n_jugada - 2, Partida.ultimas[0], Partida.ultimas[1])
                line3 = " {}. {} {} {}.*".format(Partida.n_jugada - 1, Partida.ultimas[2], Partida.ultimas[3], Partida.n_jugada - 0)

        else:
            if Partida.n_jugada == 1:
                line2 = " 1. {} {}".format(Partida.ultimas[0], Partida.ultimas[1])
                line3 = " 2. {} {}".format(Partida.ultimas[2], Partida.ultimas[3])
                Partida.evaluacion = " "
            else:
                line2 = " {}. {} {}".format(Partida.n_jugada - 1, Partida.ultimas[0], Partida.ultimas[1])
                line3 = " {}. {} {}".format(Partida.n_jugada - 0, Partida.ultimas[2], Partida.ultimas[3])

        line1 = " Analisis: {}".format(Partida.evaluacion)
        line4 = " "
        if self.color == 'blancas':
            line5 = "{} - Replicante{}.{}".format(self.perfil, self.skill, self.depth)
        else:
            line5 = "Replicante{}.{} - {}".format(self.skill, self.depth, self.perfil)
        line6 = "Ingresa jugada..."

        self.imprimirGenerico(line1, line2, line3, line4, line5, line6, seleccion=False)
        



    ### Imprimir generico
    def imprimirGenerico(self, line1=" ", line2=" ", line3=" ", line4=" ", line5=" ", line6=" ", seleccion=False, dwell=1):
        print("\n########### PANTALLA DEL USUARIO " + "############")
        print("{}\n{}\n{}\n{}\n{}\n{}\n".format(line1, line2, line3, line4, line5, line6))
        print("########### FIN PANTALLA DEL USUARIO " + "############\n")

        time.sleep(dwell)


    ### Formatear Partida
    def formatearPartida(self):
        if self.color == 'blancas':
            if len(Partida.variacion) <= 4:
                Partida.ultimas = Partida.variacion + ["*"] + ([" "] * (3 - len(Partida.variacion)))
            else:
                Partida.ultimas = Partida.variacion[-3:] + ["*"]

        else:
            if len(Partida.variacion) <= 4:
                Partida.ultimas = Partida.variacion + ["*"] + ([" "] * (3 - len(Partida.variacion)))
            else:
                Partida.ultimas = Partida.variacion[-3:] + ["*"]


    ### Menu de configuracion
    def configuracion(self):
        ### Inteligencia UCI (Modelo replicante)
        while True:
            self.imprimirGenerico('Skill level', '(0-20)')
            opcion = input()
            try:
                self.skill = int(opcion)
            except ValueError:
                self.imprimirGenerico('Opción incorrecta!', dwell=1)
                continue
            if (self.skill >= 0) & (self.skill <= 20):
                TYRELL.set_skill_level(self.skill)
                self.imprimirGenerico('Replicante', 'Skill level: {}.'.format(self.skill), dwell=0.5)
                break
            else:
                self.imprimirGenerico('Opción incorrecta!', dwell=2)


        ### Version replicante (profundidad jugada)
        while True:
            self.imprimirGenerico('Depth','(0-15)')
            opcion = input()
            try:
                self.depth = int(opcion)
            except ValueError:
                self.imprimirGenerico('Opción incorrecta!', dwell=1)
                continue
            if (self.depth >= 0) & (self.depth <= 15):
                TYRELL.set_depth(self.depth)
                self.imprimirGenerico('Replicante', 'Depth {}.'.format(self.depth), dwell=0.5)
                break
            else:
                self.imprimirGenerico('Opción incorrecta!', dwell=1)


        ### Color del jugador
        while True:
            self.imprimirGenerico('Color', '(1) Blancas', '(2) Negras', '(3) Aleatorio', '(4) Hum vs Hum', '(5) Rep vs Rep', dwell=1)
            opcion = input()
            try:
                opcion = int(opcion)
            except ValueError:
                self.imprimirGenerico('Opción incorrecta!', dwell=1)
                continue
            if (opcion >= 1) & (opcion <= 3):
                if opcion == 1:
                    self.color = 'blancas'
                elif opcion == 2:
                    self.color = 'negras'
                elif opcion == 3:
                    self.color = random.choice(['blancas', 'negras'])

                self.imprimirGenerico('Color', '{}.'.format(self.color), dwell=0.5)
                break

            else:
                self.imprimirGenerico('Opción incorrecta!', dwell=2)



    def crearPerfil(self):
        while True:
            self.imprimirGenerico('INICIO', '(1) Cargar perfil', '(2) Jugar partida', dwell=0.5)
            opcion = input()
            try:
                opcion = int(opcion)
            except ValueError:
                self.imprimirGenerico('Opción incorrecta!', dwell=1)
                continue
            if (opcion >= 1) & (opcion <= 2):
                if opcion == 1:
                    self.leerPartida(tipo='juego')
                if opcion == 2:
                    self.perfil = "Intruso"
                    self.configuracion()
                #self.imprimirGenerico("Perfil:", "{}", "Color:", "{}.".format(self.perfil, self.color), dwell=0.5)
                return

            else:
                self.imprimirGenerico('Opción incorrecta!', dwell=2)


#################
    ### Guardar juego
    def escribirPartida(self, tipo):
        # Crea diccionario con header y arbol (implementar PGN)
        partida = dict(header=self.header, variacion=Partida.variacion, n_jugada=Partida.n_jugada,
                           n_movimiento=Partida.n_movimiento, evaluacion=Partida.evaluacion,
                           jugada_correcta=Partida.jugada_correcta, color=self.color, skill=self.skill,
                           depth=self.depth, contempt=self.contempt, pgn = [])

        # Nombre del perfil donde guardar la partida
        self.imprimirGenerico("Escribe nombre perfil:", "a: (A)trás")
        perfiles = glob.glob('perfiles/*.gm')

        # Imprime lista de perfiles
        nombres_perfiles = [i.split('/')[-1][:-3] for i in perfiles]
        for linea in nombres_perfiles:
            print("-> {}".format(linea))

        # Espera string especificando nombre del perfil
        opcion = input()
        if opcion != "a":
            if self.color == 'blancas':
                nombre_partida = "{}-Replicante{}.{} {}".format(opcion, partida['depth'], partida['skill'], partida['header']['fecha'])
            else:
                nombre_partida = "Replicante{}.{}-{} {}".format(partida['depth'], partida['skill'], opcion, partida['header']['fecha'])

            try:
                diccionario = pickle.load(open('perfiles/{}.gm'.format(opcion), 'rb'))
            except FileNotFoundError:
                 print("[CPLs] Creando nuevo perfil {}".format(opcion))
                 diccionario = dict()
                 #self.imprimirGenerico("{}.gm".format(opcion), "no existe...", dwell=1)

            print("Diccionario cargado {}:\n{}".format(opcion, diccionario.keys()))
            diccionario[nombre_partida] = partida
            pickle.dump(diccionario, open('perfiles/{}.gm'.format(opcion), 'wb'))
            print("Diccionario creado {}:\n{}".format(opcion, diccionario.keys()))

            self.imprimirGenerico("Guardado en", "{} !!".format(opcion))
            time.sleep(2)

   #Prueba
   ### Leer partida
    def leerPartida(self, tipo):
        ### Carga perfil
        self.imprimirGenerico("Nombre del perfil:")
        perfiles = glob.glob('perfiles/*.gm')
        if len(perfiles) == 0:
            self.imprimirGenerico("No hay perfiles", " ", "CONSEJO:", "Guarda un juego nuevo", "para crear tu primer perfil.")
            self.crearPerfil()

        # Imprime lista de perfiles
        nombres_perfiles = [i.split('/')[-1][:-3] for i in perfiles]
        for linea in nombres_perfiles:
            print("-> {}".format(linea))

        # Espera por input de usuario
        nombre_perfil = input()

        if nombre_perfil not in nombres_perfiles:
            self.imprimirGenerico("{} no existe".format(nombre_perfil))
            self.crearPerfil()
        else:
            # Intenta carga de archivo
            try:
                perfil = pickle.load(open('perfiles/{}.gm'.format(nombre_perfil), 'rb'))
            except FileNotFoundError:
                self.imprimirGenerico("El perfil {}".format(opcion), "No existe!", dwell=1)
                self.crearPerfil()

            ### Imprime partidas en perfil
            partidas = list(perfil.keys())
            print("[CPLs] Partidas en perfil:")
            iterador = 1
            for line in partidas:
                print("({}) {}".format(iterador, line))
                iterador += 1

            self.imprimirGenerico("Selecciona partida:", "(INGRESA SOLO NUMEROS!)")
            try:
                opcion = int(input())
            except ValueError:
                self.imprimirGenerico("Opción {}".format(opcion), "incorrecta !!")
                self.crearPerfil()
                #return

            print("Selección: {}".format(opcion))
            print("Numero partidas: {}".format(len(partidas)))
            if (opcion > 0) & (opcion < (len(partidas) + 1)):
                partida = partidas[opcion - 1]
                diccionario = perfil[partida]

                Partida.header          = diccionario['header']
                Partida.variacion       = diccionario['variacion']
                Partida.n_jugada        = diccionario['n_jugada']
                Partida.n_movimiento    = diccionario['n_movimiento']
                Partida.evaluacion      = diccionario['evaluacion']
                Partida.jugada_correcta = diccionario['jugada_correcta']
                self.color              = diccionario['color']
                self.skill              = diccionario['skill']
                self.depth              = diccionario['depth']
                self.contempt           = diccionario['contempt']
                self.perfil             = nombre_perfil
                self.imprimirGenerico("Perfil {}".format(self.perfil), "Partida {}".format(partida), "Cargados exitosamente!")
            else:
                self.imprimirGenerico("La opción {}".format(opcion), "Es incorrecta.", dwell=2)
                self.crearPerfil()

            Motor.set_position(Partida.variacion)
            #print(stockfish.get_board_visual())
            #time.sleep(2)


    def tableroFEN(self):
        TYRELL.set_position(Partida.variacion)
        fen = TYRELL.get_fen_position()
        tablero_fen = ""
        unicode = Partida.diccionario_unicode
        for pieza in fen:
            if pieza in unicode.keys():
                tablero_fen += unicode[pieza]
            elif pieza == " ":
                break
            else:
                tablero_fen += '\n'

        print(tablero_fen)



    def posicionTablero(self, color='b'):
        coordenadas = [
'a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8',
'a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7',
'a6', 'b6', 'c6', 'd6', 'e6', 'f6', 'g6', 'h6',
'a5', 'b5', 'c5', 'd5', 'e5', 'f5', 'g5', 'h5',
'a4', 'b4', 'c4', 'd4', 'e4', 'f4', 'g4', 'h4',
'a3', 'b3', 'c3', 'd3', 'e3', 'f3', 'g3', 'h3',
'a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2',
'a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1'
]

        unicode = Partida.diccionario_unicode

        TYRELL.set_position(Partida.variacion)
        fen = TYRELL.get_fen_position()
        fen = fen.split(' ')

        tablero = []
        for letra in fen[0]:
            if letra in ["1", "2", "3", "4", "5", "6", "7", "8"]:
                tablero.extend(["." for i in range(int(letra))])
            elif letra == "/":
                pass
            else:
                tablero.append(letra)

        piezas = ['k', 'q', 'r', 'b', 'n', 'p']

        if color == 'b':
            piezas = [pieza.upper() for pieza in piezas]

        for pieza in piezas:
            posicion = []

            for index in range(len(tablero)):
                if tablero[index] == pieza:
                    posicion.append(coordenadas[index])

            print("{} {}".format(unicode[pieza], posicion))

