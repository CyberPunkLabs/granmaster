### Importa modulos requieridos por Gran Master
import sys
import os
import glob
import time
import pickle
import random

import Keys
import Lcd
import Framebuffer
import Font
import Menu
import Log
import Move

import numpy as np
from datetime import datetime
from models import Stockfish

#sys.path.insert(1, "/home/diogenes/projects/granmaster/lcd/")

os.system("xhost si:localuser:root")
# [ERROR] Solucionado con xhost si:localuser:root
lcd = Lcd.Lcd()
keyEvent = Keys.KeyEvent()
font = Font.Font('FONTS/BIGPILE/SEEMORE/CM-6X6.F06')
log = Log.Log(font)
out_device = 'terminal'


### Crea a Tyrell, como instancia de Stockfish, con:
### PV: 4; arrogancia: 0; habilidad: 20; profundidad de analisis = 20 
if os.name == 'nt':
    engine_path = "./engine/stockfish_20011801_x64.exe"
else: ### definir directorio propio !!
    engine_path = "/usr/games/stockfish"

TYRELL = Stockfish(engine_path, parameters={"MultiPV": 4, "Contempt": 0})
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
    tipo = 'blancas'
    habilidad = 1
    profundidad_analisis = 1


    ### Pantalla de inicio. Revisar si adecuado declararla en __init__
    def __init__(self):
        ### Despliega pantallas de configuracion
        #self.crearPerfil()
        #self.arrogancia = 0
        self.color = "blancas"
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


        
################## INICIO MENUES CONFIGURACION #####################

    ### Crear de inicio ###                
    def menuInicio(self):
        lineas = ["Partida:", "Nuevo", "Cargar"]
        opcion = self.imprimirGenerico(lineas, opciones=[1,2])
        print("Seleccion (inicio): {} (tipo: {})".format(opcion, type(opcion)))

        try:
            opcion = int(opcion) # casting to int will likely raise an error
            #print("Opcion (inicio): {} (tipo: {})".format(opcion, type(opcion)))
            if opcion in [1, 2]:
                if opcion == 1:
                    self.perfil = "Intruso"
                    self.menuConfiguracion()
                if opcion == 2:
                    #self.leerPartida(tipo='juego')
                    self.menuInicio()
            else:
                lineas = ['Opción', 'incorrecta!']
                self.imprimirGenerico(lineas, seleccion=False)
                self.menuInicio()

        except ValueError:
            lineas = ['Value error!']
            self.imprimirGenerico(lineas, seleccion=False)
            self.menuInicio()
            

    ### Menu de configuracion
    def menuConfiguracion(self):
        ### Color del jugador
        lineas = ["Tipo:", "Blancas", "Negras (no)", "Aleatorio (no)", "Apertura (no)", "Rep vs Rep (no)"]
        opcion = self.imprimirGenerico(lineas, opciones=[1], seleccion=True)
        #print("Seleccion (juego): {} (opcion: {})".format(lineas(opcion), opcion))
        #opcion = input()
        try:
            opcion = int(opcion)
            
            if opcion in [1]:
                if opcion == 1:
                    Partida.tipo = 'blancas'
                    self.color = 'blancas'
                elif opcion == 2:
                    Partida.tipo = 'blancas'
                    self.color = 'negras'
                elif opcion == 3:
                    Partida.tipo = 'blancas'
                    self.color = random.choice(['blancas', 'negras'])

                lineas = ["Color: ", "{}.".format(self.color)]
                self.imprimirGenerico(lineas, seleccion=False)
                self.menuHabilidad()
                self.menuProfundidad()
            else:
                self.imprimirGenerico(["Opción no implementada..."], seleccion=False)
                self.menuConfiguracion()

        except ValueError:
            lineas = ['Value error!']
            self.imprimirGenerico(lineas, seleccion=False)
            self.menuConfiguracion()


    ### Inteligencia UCI: Habilidad replicante. Stockfish.set_skill_level [0, 20]
    def menuHabilidad(self):
        lineas = ["Habilidad", "Replicante:", "1", "2"]
        opcion = self.imprimirGenerico(lineas, opciones=[2,3])

        try:
            self.habilidad = int(opcion)
            if (self.habilidad >= 1) & (self.habilidad <= 20):
                lineas = ['Replicante', 'Habilidad: {}.'.format(self.habilidad-1)]
                self.imprimirGenerico(lineas, seleccion=False)
            else:
                lineas = ['Opcion', 'incorrecta!']
                self.imprimirGenerico(lineas, seleccion=False)
                self.menuHabilidad()

        except ValueError:
            lineas = ['Value error!']
            self.imprimirGenerico(lineas, seleccion=False)
            self.menuHabilidad()


    ### Profundidad de analisis (numero de iteraciones efectuadas por Replicante)
    def menuProfundidad(self):
        lineas = ["Profundidad", "análisis", "1", "2"]
        opcion = self.imprimirGenerico(lineas, opciones=[2,3])

        try:
            self.profundidad_analisis = int(opcion)

            if (self.profundidad_analisis >= 1) & (self.profundidad_analisis <= 40):
                lineas = ['Replicante', 'Profundidad: {}.'.format(self.profundidad_analisis-1)]
                self.imprimirGenerico(lineas, seleccion=False)        
            else:
                self.imprimirGenerico(['Opción incorrecta!'], seleccion=False)
                self.menuProfundidad()
                    
        except ValueError:
            lineas = ['Value error!']
            self.imprimirGenerico(lineas, seleccion=False)
            self.menuProfundidad()




################## INICIO MENUES DE PARTIDA #####################
    ### Maneja las opciones del juego
    def opciones(self):
        lineas = ["Análisis", "Deshacer", "Posición blancas", "Posición negras"]
        entrada = self.imprimirGenerico(lineas)

        print("Entrada: {}".format(entrada))

        
        # # Imprime el analisis de Tyrell (Stockfish depth:15, skill:20, PV:4)
        # if entrada == "a":
        #     self.imprimirAnalisis()
        # elif entrada == "t":
        #     TYRELL.set_position(Partida.variacion)
        #     print(TYRELL.get_board_visual())
        # # Deshace la jugada
        # elif entrada == "d":
        #     self.deshacer()
        # # Escribe la partida en un perfil de usuario
        # #elif entrada == "e":
        # #    self.escribirPartida(tipo='juego')
        # # Imprime el tablero en letras (desarrolladores)
        # elif entrada == "p":
        #     TYRELL.set_position(Partida.variacion)
        #     print(TYRELL.get_board_visual())
        # # Imprime posicion FEN
        # #elif entrada == "f":
        # #    print("[CPLs] Posición FEN:")
        # #    print(TYRELL.get_fen_position())
        # # Imprime la posicion de las blancas o negras
        # elif entrada in ["b", "n"]:
        #     self.posicionTablero(color=entrada)
        # # Lee la partida un un perfil guardado
        # #elif entrada == "l":
        # #    self.leerPartida(tipo='juego')

        # # Ante una opcion incorrecta:
        # #else:

        # # Con LCD, hace titilar la pantalla
        # #self.titilar()
        Partida.jugada_correcta = False


        
    ### Imprimir pantalla principal, con la informacion central de la partida
    def imprimirPartida(self):
        evaluacion = self.evaluarPartida()
        self.formatearPartida()

        # Formatea las líneas
        if self.color == 'blancas':
            if Partida.n_jugada == 1:
                linea2 = "1. {} {}".format(Partida.ultimas[0], Partida.ultimas[1])
                linea3 = "2. {} {}".format(Partida.ultimas[2], Partida.ultimas[3])
            elif Partida.n_jugada == 2:
                linea2 = "1. {} {}".format(Partida.ultimas[0], Partida.ultimas[1])
                linea3 = "2. {} {}".format(Partida.ultimas[2], Partida.ultimas[3])
            else:
                linea2 = "{}. {} {}".format(Partida.n_jugada - 2, Partida.ultimas[0], Partida.ultimas[1])
                linea3 = "{}. {} {} {}.*".format(Partida.n_jugada - 1, Partida.ultimas[2], Partida.ultimas[3], Partida.n_jugada - 0)

        else:
            if Partida.n_jugada == 1:
                linea2 = "1. {} {}".format(Partida.ultimas[0], Partida.ultimas[1])
                linea3 = "2. {} {}".format(Partida.ultimas[2], Partida.ultimas[3])
            else:
                linea2 = "{}. {} {}".format(Partida.n_jugada - 1, Partida.ultimas[0], Partida.ultimas[1])
                linea3 = "{}. {} {}".format(Partida.n_jugada - 0, Partida.ultimas[2], Partida.ultimas[3])

        linea1 = "Análisis: {}".format(Partida.evaluacion)
        linea4 = " "

        
        if Partida.tipo == 'apertura':
            if self.color == 'blancas':
                linea5 = "{} - {}".format(self.perfil, Partida.nombre_apertura.title())
            else:
                linea5 = "{} - {}".format(Partida.nombre_apertura.title(), self.perfil)

            linea5 = "Ingresa jugada..."
            linea6 = "Opciones"
            lineas = [linea1, linea2, linea3, linea4, linea5, linea6]
            self.imprimirGenerico(lineas, seleccion=True)

        else:
            if self.color == 'blancas':
                linea5 = "{} - Replicante{}.{}".format(self.perfil, self.habilidad, self.profundidad_analisis)
            else:
                linea5 = "Replicante{}.{} - {}".format(self.habilidad, self.profundidad_analisis, self.perfil)

            linea5 = "Ingresa jugada..."
            linea6 = "Opciones"
            lineas = [linea1, linea2, linea3, linea4, linea5, linea6]
            opcion = self.imprimirGenerico(lineas, [4], seleccion=False)

            print("la opcion: {}".format(opcion))


            return opcion

            

################# EVALUACIONES Y ANALISIS ###################
    def evaluarPartida(self):
        ### Tyrell evalua la posicion en centipeones
        TYRELL.set_position(Partida.variacion)
        evaluacion = TYRELL.get_evaluation()
        evaluacion = evaluacion['value'] / 100
        if self.color == 'negras':
            evaluacion = evaluacion * -1

        # Estandariza el string de salida a +/-x.xx
        if evaluacion >= 0:
            Partida.evaluacion = "+{:.2f}".format(evaluacion)
        else:
            Partida.evaluacion = "{:.2f}".format(evaluacion)

        return evaluacion
    

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
                    
        lineas = ["[Análisis]", "{} {}".format(evaluacion[0], variacion[0]), "{} {}".format(evaluacion[1], variacion[1]),
                  "{} {}".format(evaluacion[2], variacion[2]), "{} {}".format(evaluacion[3], variacion[3])]
                    
        self.imprimirGenerico(lineas)



########## OPERACIONES SOBRE PARTIDA ####################        
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
            lineas = ["No hay más jugadas", "que deshacer!"]
            self.imprimirGenerico("No hay más jugadas", "que deshacer!")
            
        # Reimprime la partida
        self.imprimirPartida()

        

##################### FUNCIONES DE IMPRESION ######################

    def imprimirLCD(self, lineas, opciones, move=False):
        print("Entrando a LCD")

        if move:
            move = Move.Move(lcd, keyEvent, font)
            opcion = move.run()
        else:
            menu = Menu.Menu(lcd, keyEvent, font, lineas, opciones, 0)
            opcion = menu.run()

        print("Opt: {}".format(opcion))
        return opcion


    ### Imprimir generico
    def imprimirGenerico(self, lineas, opciones=[0,1,2,3,4,5], move=False, seleccion=True, terminal=True, lcd=True):

        if terminal:
            print("\n### PANTALLA DEL USUARIO ")
            print(*lineas, sep="\n")

        if lcd:
            print("Salida: LCD")
            opcion = self.imprimirLCD(lineas, opciones, move)
            print("Opción: {}\nSaliendo de LCD...".format(opcion))

            return opcion
                
            
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


