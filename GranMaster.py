### Importa modulos requieridos por Gran Master
import os
import glob
import time
import pickle
import random
import numpy as np
from datetime import datetime
#from lcd5110 import LCD5110
from models import Stockfish

import Keys
import Lcd
import Framebuffer
import Font
import Menu
import Log
import Move


lcd = Lcd.Lcd()
keyEvent = Keys.KeyEvent()

font = Font.Font('FONTS/BIGPILE/SEEMORE/CM-6X8.F08')

log = Log.Log(font)


### Crea a Tyrell, como instancia de Stockfish, con:
### PV: 4; arrogancia: 0; habilidad: 20; profundidad de analisis = 20 
if os.name == 'nt':
    TYRELL = Stockfish("./engine/stockfish_20011801_x64.exe", parameters={"MultiPV": 4, "Contempt": 0})
else: ### definir directorio propio !!
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
        #self.arrogancia = 0
        self.color = 'blancas'
        self.perfil = "prueba"

        if self.color == 'blancas':
            jugador_blancas = self.perfil,
            jugador_negras = 'Replicante' #{}.{}'.format(self.profundidad_analisis, self.habilidad),
        else:
            jugador_negras = self.perfil,
            jugador_blancas = 'Replicante' #{}.{}'.format(self.profundidad_analisis, self.habilidad),

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
        print(Partida.n_movimiento)
        print(Partida.apertura[Partida.n_movimiento])
        if (len(entrada) > 1) & (TYRELL.is_move_correct(entrada)):
            if entrada != Partida.apertura[Partida.n_movimiento]:
                print("{}".format(entrada), "no es parte de la apertura")
            else:
                Partida.n_movimiento += 1
                Partida.variacion.append(entrada)

                if len(Partida.variacion) == len(Partida.apertura):
                    print("Apertura terminada")
                    self.crearPerfil()
            
                self.imprimirGenerico("Jugando", "{}".format(Partida.nombre_apertura.title()), dwell=1)

                ### Toma jugada desde libro de aperturas
                jugada = Partida.apertura[Partida.n_movimiento]

	        ### Agrega la jugada al arbol de la partida
                Partida.variacion.append(jugada)
                if len(Partida.variacion) == len(Partida.apertura):
                    print("Apertura terminada")
                    self.crearPerfil()

                Partida.n_movimiento += 1
                Partida.n_jugada += 1
                #self.evaluarPosicion()
                #self.imprimirNegras()

        ### Si la jugada no es correcta, simplementa pasa
        else:
            self.opciones(entrada)



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
        #Partida.jugada_correcta = False

        ### Si la partida tiene mas de 1 movimiento:
        if len(Partida.variacion) > 2:
            # Borra los ultimos dos
            del Partida.variacion[-2:]

            Partida.n_jugada     -= 1
            Partida.n_movimiento -= 2

        # Si no hay jugadas suficientes para deshacer
        else:
            self.imprimirGenerico("No hay más jugadas", "que deshacer!", dwell=2)

        # Reimprime la partida
        self.imprimirPartida()


    ### Imprimir pantalla principal, con la informacion central de la partida
    def imprimirPartida(self):
        ### Tyrell evalua la posicion en centipeones
        evaluacion = TYRELL.get_evaluation()
        evaluacion = evaluacion['value'] / 100
        if self.color == 'negras':
            evaluacion = evaluacion * -1
        # Estandariza el string de salida a +/-x.xx
        if evaluacion >= 0:
            Partida.evaluacion = "+{:.2f}".format(evaluacion)
        else:
            Partida.evaluacion = "{:.2f}".format(evaluacion)

        self.formatearPartida()

        if self.color == 'blancas':
            if Partida.n_jugada == 1:
                line2 = " 1. {} {}".format(Partida.ultimas[0], Partida.ultimas[1])
                line3 = " 2. {} {}".format(Partida.ultimas[2], Partida.ultimas[3])
                #Partida.evaluacion = " "
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
                #Partida.evaluacion = " "
            else:
                line2 = " {}. {} {}".format(Partida.n_jugada - 1, Partida.ultimas[0], Partida.ultimas[1])
                line3 = " {}. {} {}".format(Partida.n_jugada - 0, Partida.ultimas[2], Partida.ultimas[3])

        line1 = " Analisis: {}".format(Partida.evaluacion)
        line4 = " "
        if Partida.tipo == 'apertura':
            if self.color == 'blancas':
                line5 = "{} - {}".format(self.perfil, Partida.nombre_apertura.title())
            else:
                line5 = "{} - {}".format(Partida.nombre_apertura.title(), self.perfil)
            line6 = "Ingresa jugada..."
            self.imprimirGenerico(line1, line2, line3, line4, line5, line6, seleccion=False)
        
        else:
            if self.color == 'blancas':
                line5 = "{} - Replicante{}.{}".format(self.perfil, self.habilidad, self.profundidad_analisis)
            else:
                line5 = "Replicante{}.{} - {}".format(self.habilidad, self.profundidad_analisis, self.perfil)
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

                
    #############################
    ### Menu de configuracion
    def configuracion(self):
        ### Color del jugador
        while True:
            self.imprimirGenerico('Color', '(1) Blancas', '(2) Negras', '(3) Aleatorio', '(4) Apertura', '(5) Rep vs Rep', dwell=1)
            opcion = input()
            try:
                opcion = int(opcion)
            except ValueError:
                self.imprimirGenerico('Opción incorrecta!', dwell=1)
                continue
            if opcion == 1:
                Partida.tipo = 'blancas'
                self.color = 'blancas'
                break
            elif opcion == 2:
                Partida.tipo = 'blancas'
                self.color = 'negras'
                break
            elif opcion == 3:
                Partida.tipo = 'blancas'
                self.color = random.choice(['blancas', 'negras'])            
                self.imprimirGenerico('Color', '{}.'.format(self.color), dwell=0.5)
                break
            elif opcion == 4:
                Partida.tipo = 'apertura'
                aperturas = Partida.aperturas.keys()
                print("Elige apertura:")
                for apertura in aperturas:
                    print(apertura)
                nombre_apertura = input()
                if nombre_apertura not in aperturas:
                    self.imprimirGenerico("{} no existe".format(nombre_apertura))
                    self.crearPerfil()
                else:
                    Partida.nombre_apertura = nombre_apertura
                    Partida.apertura = Partida.aperturas[nombre_apertura]
                    print("Elegiste {}".format(nombre_apertura))
                    print(Partida.apertura)
                    time.sleep(3)
                    break
            else:
                self.imprimirGenerico('Opción no implementada...', dwell=2)


        if not Partida.tipo == 'apertura':
            ### Inteligencia UCI: Habilidad replicante. Stockfish.set_skill_level [0, 20]
            while True:
                self.imprimirGenerico('Habilidad Replicante', '(1-20)')
                opcion = input()
                try:
                    self.habilidad = int(opcion)
                except ValueError:
                    self.imprimirGenerico('Opción incorrecta!', dwell=1)
                    continue
                if (self.habilidad >= 1) & (self.habilidad <= 20):
                    self.imprimirGenerico('Replicante', 'Habilidad: {}.'.format(self.habilidad), dwell=0.5)
                    break
                else:
                    self.imprimirGenerico('Opción incorrecta!', dwell=2)


            ### Profundidad de analisis (numero de iteraciones efectuadas por Replicante)
            while True:
                self.imprimirGenerico('Profundidad análisis','(1-40)')
                opcion = input()
                try:
                    self.profundidad_analisis = int(opcion)
                except ValueError:
                    self.imprimirGenerico('Opción incorrecta!', dwell=1)
                    continue
                if (self.profundidad_analisis >= 1) & (self.profundidad_analisis <= 40):
                    self.imprimirGenerico('Replicante', 'Profundidad: {}.'.format(self.profundidad_analisis), dwell=1)
                    #self.imprimirGenerico('Replicante', 'Arrogancia: {}.'.format(self.arrogancia), dwell=1)
                    break
                else:
                    self.imprimirGenerico('Opción incorrecta!', dwell=1)




                
    def crearPerfil(self):
        menuOptions = ['Jugar', 'Rendirse', 'Salir', 'Ayuda', '1', '2']
        move = Move.Move(lcd, keyEvent, font)
        menu = Menu.Menu(lcd, keyEvent, font, ['Cargar perfil', 'Jugar partida'], 0)

        selection = menu.run()
        if selection == 0:
            self.leerPartida(tipo='juego')
        if selection == 1:
            self.perfil = "Intruso"
            self.configuracion()

        return


#################
    ### Guardar juego
    def escribirPartida(self, tipo):
        # Crea diccionario con header y arbol (implementar PGN)
        partida = dict(header=self.header, variacion=Partida.variacion, n_jugada=Partida.n_jugada,
                           n_movimiento=Partida.n_movimiento, evaluacion=Partida.evaluacion,
                           jugada_correcta=Partida.jugada_correcta, color=self.color, habilidad=self.habilidad,
                           profundidad_analisis=self.profundidad_analisis, arrogancia=self.arrogancia, pgn = [])

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
                nombre_partida = "{}-Replicante{}.{} {}".format(opcion, partida['profundidad_analisis'], partida['habilidad'], partida['header']['fecha'])
            else:
                nombre_partida = "Replicante{}.{}-{} {}".format(partida['profundidad_analisis'], partida['habilidad'], opcion, partida['header']['fecha'])

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
                self.color                  = diccionario['color']
                self.habilidad              = diccionario['habilidad']
                self.profundidad_analisis   = diccionario['profundidad_analisis']
                self.arrogancia             = diccionario['arrogancia']
                self.perfil                 = nombre_perfil
                self.imprimirGenerico("Perfil {}".format(self.perfil), "Partida {}".format(partida), "Cargados exitosamente!")
            else:
                self.imprimirGenerico("La opción {}".format(opcion), "Es incorrecta.", dwell=2)
                self.crearPerfil()

            TYRELL.set_position(Partida.variacion)
            #print(stockfish.get_board_visual())
            #time.sleep(2)


    def imprimirTablero(self):
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



    ### Maneja las opciones del juego
    def opciones(self, entrada):
        # Imprime el analisis de Tyrell (Stockfish depth:15, skill:20, PV:4)
        if entrada == "a":
            self.imprimirAnalisis()
        # Imprime el tablero en lindas figuras Unicode
        elif entrada == "t":
            print("[CPLs] Tablero:")
            self.imprimirTablero()
            print("\n")
        # Deshace la jugada
        elif entrada == "d":
            self.deshacer()
        # Escribe la partida en un perfil de usuario
        elif entrada == "e":
            self.escribirPartida(tipo='juego')
        # Imprime el tablero en letras (desarrolladores)
        elif entrada == "p":
            TYRELL.set_position(Partida.variacion)
            print(TYRELL.get_board_visual())
        # Imprime posicion FEN
        elif entrada == "f":
            print("[CPLs] Posición FEN:")
            print(TYRELL.get_fen_position())
        # Imprime la posicion de las blancas o negras
        elif entrada in ["b", "n"]:
            self.posicionTablero(color=entrada)
        # Lee la partida un un perfil guardado
        elif entrada == "l":
            self.leerPartida(tipo='juego')

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
