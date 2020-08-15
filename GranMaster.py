### Importa modulos requieridos por Gran Master
import time
import pickle
import random

from lcd5110 import LCD5110
from stockfish import Stockfish


### Declara stockfish y control sobre pantalla LCD
stockfish = Stockfish("/usr/games/stockfish", parameters={'Contempt': 0})
#print(stockfish.get_parameters())
lcd = LCD5110()


#### DEBERIA LLAMARSE PARTIDA!!
### Clase principal
class Juego:

    ''' Llama a stockfish y efectua e imprime la jugada.

[Historial]

[Pendiente]
-> Auditar la evaluacion de la jugada. Intentar actualizarla cada ej 3 s 


'''

    ### Construye header con info sobre la partida (por implementar)
    header = dict(
        evento = 'Partida CyberPunkChess',
        lugar = 'Laboratorios CyberPunk',
        fecha = '20 abril 2020',
        ronda = 1,
        jugador_blancas = 'Perfil 1',
        jugador_negras = 'Stockfish Level {} Depth {}'.format(10, 30), # DECLARARLO MAS ADELANTE !!
        resultado = '*/*')


    ### Declara variables basicas
    juego = []
    n_movimiento = 0
    n_jugada = 1
    jugada_correcta = True
    salir = False
    lcd_on = True
    lcd.backlight(True)


    ### Pantalla de inicio. Revisar si adecuado declararla asi
    def __init__(self):

        line2 = '#' * 17
        line3 = '#  Bienvenido   #'
        line4 = '#     v.0.1     #'
        line5 = '#' * 17


        ### Despliega pantallas de configuracion
        #self.configuracion()           
        self.color = 'n'

        
        
##################       Inicio del loop principal         #####################
    def jugada(self):
        ### Para las blancas ###
        if self.color == 'b':
            pass
        
        ### Para las negras ###
        else:
            ### Construye arbol de aperturas de los top 10 GMs
            aperturas = ['e2e4'] * 43 + ['d2d4'] * 38 + ['g1f3'] * 10 + ['c2c4'] * 8\
                + [random.choice(['b2b3', 'g2g3', 'f2f4', 'b1c3', 'e2e3'])]

            ### Si la jugada anterior de las negras es correcta:
            if Juego.jugada_correcta:
                self.imprimirGenerico('Replicante 0.1', 'esta pensando...')
                time.sleep(1)

                ### Si es la jugada 1, elige jugada del arbol de aperturas
                if Juego.n_jugada == 1:
                    blancas = random.choice(aperturas)

                ### Si la jugada es > 1, juega Stockfish    
                else:
                    clock = time.time()

                    ### Toma jugada de best_move dado nivel y profundidad
                    blancas = stockfish.get_best_move()

                    ### Alternativamente, podria tomarla de best_move_time dado limite temporal
                    #blancas = stockfish.get_best_move_time(2000)
                    print('Jugada en {} s.'.format(time.time() - clock))

                ### Agrega la jugada al arbol del juego     
                Juego.juego.append(blancas)
                Juego.n_movimiento += 1

                ### Fija posicion en el tablero y evalua la posicion
                stockfish.set_position(Juego.juego)
                evaluacion = stockfish.get_evaluation()
                Juego.evaluacion = evaluacion['value'] / 100

            ### Envia info a LCD    
            self.imprimirNegras()            
            print(stockfish.get_board_visual())
            
            ### Espera por input de las negras
            negras = input().lower()
            
            ### Respuestas al input
            # Si existe input y este es una jugada correcta
            if (len(negras) > 1) & (stockfish.is_move_correct(negras)):
                Juego.juego.append(negras)

                stockfish.set_position(Juego.juego)

                Juego.n_movimiento += 1
                Juego.n_jugada += 1

                Juego.jugada_correcta = True
                self.guardarJuego('respaldo')
                self.imprimirNegras()

            # Guardar juego    
            elif negras == 's':
                self.guardarJuego('juego')
                Juego.jugada_correcta = False

            # Deshacer jugada
            elif negras == 'a':
                self.deshacer()
                Juego.jugada_correcta = False

            # Opciones
            elif negras == 'o':
                self.imprimirOpciones()
                Juego.jugada_correcta = False

            # Encender luz (CAMBIAR A OPCIONES!!)   
            elif negras == 'l':
                lcd.backlight(self.lcd_on)
                self.lcd_on = not self.lcd_on
                Juego.jugada_correcta = False

            # Input no reconocido
            else:
                self.imprimirGenerico('{} incorrecta!'.format(negras))
                Juego.jugada_correcta = False

                time.sleep(2)
                


##################               PANTALLAS              #####################

    ### Deshacer jugada
    def deshacer(self):
        ### Si en el juego hay mas de 1 jugada:
        if len(Juego.juego) > 1:
            # Borra las ultimas dos
            del Juego.juego[-2:]

            # Fija posicion y reevalua
            stockfish.set_position(Juego.juego)
            evaluacion = stockfish.get_evaluation()
            Juego.evaluacion = evaluacion['value'] / 100

            Juego.n_jugada     -= 1
            Juego.n_movimiento -= 2

        # Si no hay jugadas suficientes para deshacer    
        else:
            self.imprimirGenerico("No hay mas jugadas", "que deshacer!")
            time.sleep(1)


    ### Guardar juego
    def guardarJuego(self, tipo):
        # Crea diccionario con header y arbol (implementar PGN)
        diccionario = dict(header=Juego.header, juego=Juego.juego, n_jugada=Juego.n_jugada,
                           n_movimiento=Juego.n_movimiento, evaluacion=Juego.evaluacion,
                           jugada_correcta=Juego.jugada_correcta, color=self.color, pgn=[])

        # Si es con opcion de grabado automatico (respaldo)
        if tipo == 'respaldo':
            pickle.dump(diccionario, open('juegos/{}.gm'.format(tipo), 'wb'))

        # Si no, pregunta donde guardar el juego:
        else:
            perfiles = ['perfil1', 'perfil2', 'perfil3', 'perfil4', 'perfil5']

            #-------------------  
            opcion = self.imprimirGenerico("Guardar en:", "(1) Perfil", "(2) Perfil",
                                  "(3) Perfil", "(4) Perfil", "(5) Perfil", seleccion=True)

            
            #opcion = input()
            opcion = perfiles[int(opcion) - 1]
            
            pickle.dump(diccionario, open('juegos/{}.gm'.format(opcion), 'wb'))
            
            self.imprimirGenerico("Guardado en", "{}.gm !!".format(opcion))
            time.sleep(2)

            


    ### Cargar juego
    def cargarJuego(self, tipo):

        if tipo == 'respaldo':
            try:
                diccionario = pickle.load(open('juegos/{}.gm'.format(tipo), 'rb'))
                
                Juego.header          = diccionario['header']
                Juego.juego           = diccionario['juego']
                Juego.n_jugada        = diccionario['n_jugada']
                Juego.n_movimiento    = diccionario['n_movimiento']
                Juego.evaluacion      = diccionario['evaluacion']
                Juego.jugada_correcta = diccionario['jugada_correcta']
                self.color            = diccionario['color']

            except FileNotFoundError:
                self.imprimirGenerico("respaldo.gm", "no existe...")
                

        else:
            perfiles = ['perfil1', 'perfil2', 'perfil3', 'perfil4', 'perfil5']

            #-------------------  
            opcion = self.imprimirGenerico("Cargar perfil:", "(1) Perfil", "(2) Perfil",
                                  "(3) Perfil", "(4) Perfil", "(5) Perfil", seleccion=True)
            
            
            #opcion = input()
            opcion = perfiles[int(opcion) - 1]

            try:
                diccionario = pickle.load(open('juegos/{}.gm'.format(opcion), 'rb'))

                Juego.header          = diccionario['header']
                Juego.juego           = diccionario['juego']
                Juego.n_jugada        = diccionario['n_jugada']
                Juego.n_movimiento    = diccionario['n_movimiento']
                Juego.evaluacion      = diccionario['evaluacion']
                Juego.jugada_correcta = diccionario['jugada_correcta']
                self.color            = diccionario['color']

                self.imprimirGenerico("Juego cargado", "'{}.gm'!!".format(opcion))
                
            except FileNotFoundError:
                self.imprimirGenerico("{}".format(opcion), "no existe...")
                            

        stockfish.set_position(Juego.juego)
        #print(stockfish.get_board_visual())
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
            self.imprimirGenerico('Gran Master', line3='(1) Nuevo', line4='(2) Perfil')

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


    ### Imprimir pantalla para negras            
    def imprimirNegras(self):
        self.formatearJuego()
    
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
        # 1 ver 2 variante 3 analisis 4 cargar 5 salir 6 APERTURAS

        #-------------------
        line1 = "OPCIONES"  
        line2 = "(1) Volver" # Cambiar a que se pueda hacer scroll por el juego completo
        line3 = "(2) Variante"
        line4 = "(3) Analisis"
        line5 = "(4) Cargar"
        line6 = "(5) Salir" # AGREGAR "MAS OPCIONES"

        v = 1
        h = 1
        vector_inversion = [False, True, False, False, False, False]
        volver = False
        while not volver:
            lcd.clear()
            
            lcd.cursor(1,1)
            lcd.inverse(vector_inversion[0])              
            lcd.printStr(line1)

            lcd.cursor(2, 1)
            lcd.inverse(vector_inversion[1])
            lcd.printStr(line2)

            lcd.cursor(3, 1)
            lcd.inverse(vector_inversion[2])
            lcd.printStr(line3)

            lcd.cursor(4, 1)
            lcd.inverse(vector_inversion[3])
            lcd.printStr(line4)

            lcd.cursor(5, 1)
            lcd.inverse(vector_inversion[4])
            lcd.printStr(line5)

            lcd.cursor(6, 1)
            lcd.inverse(vector_inversion[5])
            lcd.printStr(line6)
            lcd.inverse(False)

            print("v = {}".format(v))
            print("h = {}".format(h))
            ### Espera por input
            opcion = input()

            if opcion == '2':
                v += 1
                if v > 5:
                    v = 1
                    
            elif opcion == '4':
                h += 1
                if h > 5:
                    h = 1
                    
            elif opcion == '8':
                v -= 1
                if v < 1:
                    v = 5
                    
            elif opcion == '6':
                h -= 1
                if h > 1:
                    h = 5

            ### Volver al juego
            elif opcion == 'o':
                if v == 4:
                    self.cargarJuego('juego')
                    volver = True

                elif v == 1:
                    volver = True

            else:
                self.imprimirGenerico('No reconocida...')
                time.sleep(1)

            vector_inversion = [False, False, False, False, False, False]                
            vector_inversion[v] = True
            print(vector_inversion)
                            

    ### Imprimir generico
    def imprimirGenerico(self, line1=" ", line2=" ", line3=" ", line4=" ", line5=" ", line6=" ", seleccion=False):
        v = 1
        h = 1
        vector_inversion = [False, True, False, False, False, False]            
        
        while True:
            if seleccion == False:
                vector_inversion = [False, False, False, False, False, False]            

            print("Vector = {}".format(vector_inversion))
            lcd.clear()
            
            lcd.cursor(1,1)
            lcd.inverse(vector_inversion[0])              
            lcd.printStr(line1)

            lcd.cursor(2, 1)
            lcd.inverse(vector_inversion[1])
            lcd.printStr(line2)

            lcd.cursor(3, 1)
            lcd.inverse(vector_inversion[2])
            lcd.printStr(line3)

            lcd.cursor(4, 1)
            lcd.inverse(vector_inversion[3])
            lcd.printStr(line4)

            lcd.cursor(5, 1)
            lcd.inverse(vector_inversion[4])
            lcd.printStr(line5)

            lcd.cursor(6, 1)
            lcd.inverse(vector_inversion[5])
            lcd.printStr(line6)
            lcd.inverse(False)


            if seleccion == True:
                opcion = input()

                if opcion in ['8', '2']:
                    salida           = self.invertirColor(opcion, h, v, vector_inversion)
                    vector_inversion = salida[0]
                    v                = salida[1]
                    h                = salida[2]

                elif opcion == 'o':
                    break

            else:
                break

        return v
        

    ### Invertir color de lineas de la pantalla
    def invertirColor(self, opcion, h=1, v=1, vector_inversion=[False, True, False, False, False, False]):

        print("v = {}".format(v))
        print("h = {}".format(h))

        if opcion == '2':
            v += 1
            if v > 5:
                v = 1
                    
        elif opcion == '4':
            h += 1
            if h > 5:
                h = 1
                    
        elif opcion == '8':
            v -= 1
            if v < 1:
                v = 5
                    
        elif opcion == '6':
            h -= 1
            if h > 1:
                h = 5

                
        vector_inversion = [False, False, False, False, False, False]            
        vector_inversion[v] = True        
        return [vector_inversion, v, h]
        
