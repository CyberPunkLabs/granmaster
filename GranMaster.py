import time
import pickle
import random

from lcd5110 import LCD5110
from stockfish import Stockfish

stockfish = Stockfish("/usr/games/stockfish", parameters={'Contempt': 0})
#print(stockfish.get_parameters())
lcd = LCD5110()


class Juego:

    ''' Llama a stockfish y efectua e imprime la jugada.

[Historial]

[Pendiente]
-> Auditar la evaluacion de la jugada. Intentar actualizarla cada ej 3 s 


'''

    header = dict(
        evento = 'Partida CyberPunkChess',
        lugar = 'Laboratorios CyberPunk',
        fecha = '20 abril 2020',
        ronda = 1,
        jugador_blancas = 'Perfil 1',
        jugador_negras = 'Stockfish Level {} Depth {}'.format(10, 30), # DECLARARLO MAS ADELANTE !!
        resultado = '*/*')
    
    juego = []
    n_movimiento = 0
    n_jugada = 1
    jugada_correcta = True
    salir = False
    lcd_on = True
    lcd.backlight(True)


    def __init__(self):

        line2 = '#' * 17
        line3 = '#  Bienvenido   #'
        line4 = '#     v.0.1     #'
        line5 = '#' * 17

        #self.imprimirGenerico(line2=line2, line3=line3, line4=line4, line5=line5)
        #time.sleep(2)



        #self.configuracion()           
        self.color = 'n'

        
    def jugada(self):
        if self.color == 'b':
            pass
        
        ######################
        ### Para las negras
        ######################
        else:
            aperturas = ['e2e4'] * 43 + ['d2d4'] * 38 + ['g1f3'] * 10 + ['c2c4'] * 8\
                + [random.choice(['b2b3', 'g2g3', 'f2f4', 'b1c3', 'e2e3'])]

            if Juego.jugada_correcta:
                self.imprimirGenerico('Replicante 0.1', 'esta pensando...')
                time.sleep(1)

                if Juego.n_jugada == 1:
                    blancas = random.choice(aperturas)

                else:
                    clock = time.time()
                    blancas = stockfish.get_best_move()
                    print('Jugada en {} s.'.format(time.time() - clock))
                    
                Juego.juego.append(blancas)
                Juego.n_movimiento += 1
                
                stockfish.set_position(Juego.juego)

                evaluacion = stockfish.get_evaluation()
                Juego.evaluacion = evaluacion['value'] / 100


            print(stockfish.get_board_visual())
            self.imprimirNegras()
            

            negras = input().lower()

            if (len(negras) > 1) & (stockfish.is_move_correct(negras)):
                Juego.juego.append(negras)

                stockfish.set_position(Juego.juego)

                Juego.n_movimiento += 1
                Juego.n_jugada += 1

                Juego.jugada_correcta = True
                self.guardarJuego('respaldo')
                self.imprimirNegras()

            elif negras == 's':
                self.guardarJuego('juego1')
                Juego.jugada_correcta = False
                
            elif negras == 'a':
                self.deshacer()
                Juego.jugada_correcta = False

            elif negras == 'o':
                self.imprimirOpciones()
                Juego.jugada_correcta = False

            elif negras == 'l':
                lcd.backlight(self.lcd_on)
                self.lcd_on = not self.lcd_on
                Juego.jugada_correcta = False

            else:
                self.imprimirGenerico('{} incorrecta!'.format(negras))
                Juego.jugada_correcta = False

                time.sleep(2)


    ### Fin del loop principal 
    ###########################################################


    #################
    ### PANTALLAS ###
    #################

    ### Imprimir pantalla para negras            
    def imprimirNegras(self):
        self.formatearJuego()
        print("n_jugada: {}".format(Juego.n_jugada))
        print("ultimas: {}".format(Juego.ultimas))
        print("ultima: {}".format(Juego.ultimas[1]))

    
        if Juego.n_jugada == 1:
            line2 = " 1. {} {}".format(Juego.ultimas[0], Juego.ultimas[1])
            line3 = " 2. {} {}".format(Juego.ultimas[2], Juego.ultimas[3])        
        else:
            line2 = " {}. {} {}".format(Juego.n_jugada - 1, Juego.ultimas[0], Juego.ultimas[1])
            line3 = " {}. {} {}".format(Juego.n_jugada - 0, Juego.ultimas[2], Juego.ultimas[3])        


        line1 = " Analisis: {}".format(Juego.evaluacion)
        line4 = " "
        line5 = " " * 7 + "[ A G O ]"
        line6 = "Ingresa jugada..."
        print("{}\n{}\n{}\n{}\n".format(line1, line2, line3, line4, line5, line6))

        lcd.clear()
        lcd.cursor(1,1)
        lcd.printStr(line1)
        lcd.cursor(2, 1)
        lcd.printStr(line2)
        lcd.cursor(3, 1)
        lcd.printStr(line3)
        lcd.cursor(4, 1)
        lcd.printStr(line4)
        lcd.cursor(5, 1)
        lcd.printStr(line5)
        lcd.cursor(6, 1)
        lcd.printStr(line6)


    ### Imprimir opciones            
    def imprimirOpciones(self):

        #-------------------
        line1 = "OPCIONES"  
        line2 = "(1) Ver"
        line3 = "(2) Analizar"
        line4 = "(3) PGN"
        line5 = "(4) Salir"
        line6 = "(5) Unete"

        lcd.clear()
        lcd.cursor(1,1)
        lcd.printStr(line1)
        lcd.cursor(2, 1)
        lcd.printStr(line2)
        lcd.cursor(3, 1)
        lcd.printStr(line3)
        lcd.cursor(4, 1)
        lcd.printStr(line4)
        lcd.cursor(5, 1)
        lcd.printStr(line5)
        lcd.cursor(6, 1)
        lcd.printStr(line6)


        opcion = input()

        if opcion == '0':
            pass
        
        elif opcion == '4':
            self.imprimirGenerico('Juego guardado en', "'juegos/respaldo.cpc'")
            time.sleep(1)
            
            Juego.salir = True
            
        else:
            self.imprimirGenerico('Por implementar...')
            time.sleep(1)
            


    def imprimirGenerico(self, line1=" ", line2=" ", line3=" ", line4=" ", line5=" ", line6=" "):

        lcd.clear()
        lcd.cursor(1,1)
        lcd.printStr(line1)
        lcd.cursor(2, 1)
        lcd.printStr(line2)
        lcd.cursor(3, 1)
        lcd.printStr(line3)
        lcd.cursor(4, 1)
        lcd.printStr(line4)
        lcd.cursor(5, 1)
        lcd.printStr(line5)
        lcd.cursor(6, 1)
        lcd.printStr(line6)


    ### Deshacer jugada
    def deshacer(self):

        if len(Juego.juego) > 1:
            del Juego.juego[-2:]

            stockfish.set_position(Juego.juego)
            evaluacion = stockfish.get_evaluation()
            Juego.evaluacion = evaluacion['value'] / 100

            Juego.n_jugada     -= 1
            Juego.n_movimiento -= 2
               
        else:
            self.imprimirGenerico("No hay mas jugadas", "que deshacer!")
            time.sleep(1)


    ### Guardar juego
    def guardarJuego(self, tipo):

        diccionario = dict(header=Juego.header, juego=Juego.juego, pgn=[])

        if tipo == 'respaldo':
            pickle.dump(diccionario, open('juegos/{}.cpc'.format(tipo), 'wb'))

        else:
            perfiles = ['perfil1', 'perfil2', 'perfil3', 'perfil4', 'perfil5']

                                   #-------------------  
            self.imprimirGenerico("Selecciona:", "(1) Perfil", "(2) Perfil",
                                  "(3) Perfil", "(4) Perfil", "(5) Perfil")
            
            
            opcion = input()

            opcion = perfiles[int(opcion) - 1]
            
            pickle.dump(diccionario, open('juegos/{}.cpc'.format(opcion), 'wb'))

            self.imprimirGenerico("Juego guardado en", "'/juegos/{}.cpc'!!".format(opcion))
            time.sleep(2)


            
    ### Formatear juego
    def formatearJuego(self):
        
        if len(Juego.juego) <= 4:
            Juego.ultimas = Juego.juego + ["*"] + ([" "] * (3 - len(Juego.juego)))

        else:
            Juego.ultimas = Juego.juego[-3:] + ["*"]

            

    ### Menu de configuracion
    def configuracion(self):

        ### Perfil o juego nuevo
        while True:
            self.imprimirGenerico('CyberPunkChess', line3='(1) Nuevo', line4='(2) Perfil')

            opcion = input()

            try:
                opcion = int(opcion)
            except ValueError:
                self.imprimirGenerico('Opción incorrecta!')
                time.sleep(1)

                continue

            if opcion == 1:
                self.imprimirGenerico('¡Juego nuevo!')
                time.sleep(1)

                break

            elif opcion == 2:
                self.imprimirGenerico('[No implementado]')
                time.sleep(1)

            else: 
                self.imprimirGenerico('Opción incorrecta!')
                time.sleep(1)



        ### Inteligencia UCI (Modelo replicante)
        while True:
            self.imprimirGenerico('Modelo Replicante?', '(1-20)')

            opcion = input()

            try:
                opcion = int(opcion)
            except ValueError:
                self.imprimirGenerico('Opción incorrecta!')
                time.sleep(1)

                continue

            if (opcion >= 1) & (opcion <= 20):
                stockfish.set_skill_level(opcion)

                self.imprimirGenerico('Replicante', 'Modelo: {}.'.format(opcion))
                time.sleep(1)

                break

            else:
                self.imprimirGenerico('Opción incorrecta!')
                time.sleep(1)
            

        ### Version replicante (tiempo jugada)        
        while True:
            self.imprimirGenerico('Versión Replicante?','(1-30)')

            opcion = input()

            try:
                opcion = int(opcion)
            except ValueError:
                self.imprimirGenerico('Opción incorrecta!')
                time.sleep(1)

                continue

            if (opcion >= 1) & (opcion <= 30):
                stockfish.depth = opcion

                self.imprimirGenerico('Replicante', 'Versión {}.'.format(opcion))
                time.sleep(1)

                break

            else:
                self.imprimirGenerico('Opción incorrecta!')
                time.sleep(0.5)
            


        ### Color        
        while True:
            self.imprimirGenerico('Elige color', '(b) Blancas', '(n) Negras', '(a) Aleatorio')

            opcion = input().lower()

            try:
                opcion = str(opcion)
            except ValueError:
                self.imprimirGenerico('Opción incorrecta!')
                time.sleep(1)

                continue


            if opcion == 'a':
                opcion = random.choice(['b', 'n'])

                self.imprimirGenerico('Sorteando...')
                time.sleep(1)

            
            if opcion == 'b':
                self.color = 'b'

                self.imprimirGenerico('Juegas con blancas.')
                time.sleep(1)
                break

            elif opcion == 'n':
                self.imprimirGenerico('Juegas con negras.')
                time.sleep(1)
                break

            else:
                self.imprimirGenerico('¡Opción incorrecta!')
                time.sleep(1)



        self.imprimirGenerico('Iniciando juego...')
        time.sleep(3)
