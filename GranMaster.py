### Importa modulos requieridos por Gran Master
import time
import pickle
import random

from lcd5110 import LCD5110
from stockfish import Stockfish


### Declara stockfish y control sobre pantalla LCD
Motor = Stockfish("/usr/games/stockfish", parameters={'Contempt': 0})
print(Motor.get_parameters())
lcd = LCD5110()


#### DEBERIA LLAMARSE PARTIDA!!
### Clase principal
class Partida:

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
    variacion = []
    n_movimiento = 0
    n_jugada = 1
    jugada_correcta = True
    salir = False
    lcd_on = True

    
    ### Pantalla de inicio. Revisar si adecuado declararla en __init__
    def __init__(self):

        line2 = '#' * 17
        line3 = '#  Bienvenido   #'
        line4 = '#     v.0.1     #'
        line5 = '#' * 17


        ### Despliega pantallas de configuracion
        #self.configuracion()           
        self.color = 'n'

        time.sleep(0.2)
        lcd.backlight(False)
        time.sleep(0.5)
        self.imprimirGenerico(line2=line2, line3=line3, line4=line4, line5=line5, seleccion=False)
        self.titilar()

                
##################       Inicio del loop principal         #####################
    def jugada(self):
        ### Para las blancas ###
        if self.color == 'b':
            pass
        
        ### Para las negras ###
        else:
            ### Construye arbol de aperturas de los top 10 GMs
            # e2e4                        : 43%
            # d2d4                        : 38%
            # g1f3                        : 10%
            # c2c4                        : 8%
            # b2b3, g2g3, f2f4, b1c3, e2e3: 1%
            
            aperturas = ['e2e4'] * 43 + ['d2d4'] * 38 + ['g1f3'] * 10 + ['c2c4'] * 8\
                + [random.choice(['b2b3', 'g2g3', 'f2f4', 'b1c3', 'e2e3'])]

            ### Si la jugada anterior de las negras es correcta:
            if Partida.jugada_correcta:
                self.imprimirGenerico('Replicante 0.1', 'esta pensando...')
                time.sleep(1)

                ### Si es la jugada 1, elige jugada del arbol de aperturas
                if Partida.n_jugada == 1:
                    blancas = random.choice(aperturas)

                ### Si la jugada es > 1, juega Stockfish    
                else:
                    clock = time.time()

                    ### Toma jugada de best_move dado nivel y profundidad
                    blancas = Motor.get_best_move()

                    ### Alternativamente, podria tomarla de best_move_time dado limite temporal
                    #blancas = Motor.get_best_move_time(2000)
                    print('Jugada en {} s.'.format(time.time() - clock))

                ### Agrega la jugada al arbol de la partida     
                Partida.variacion.append(blancas)
                Partida.n_movimiento += 1

                ### Fija posicion en el tablero y evalua la posicion
                Motor.set_position(Partida.variacion)
                evaluacion = Motor.get_evaluation()
                Partida.evaluacion = evaluacion['value']

            ### Envia info a LCD    
            self.imprimirNegras()            
            print(Motor.get_board_visual())
            
            ### Espera por input de las negras y lo transforma a minusculas (para reconocimiento posterior)
            negras = input().lower()
            
            ### Respuestas al input
            # Si existe input y este es una jugada correcta
            if (len(negras) > 1) & (Motor.is_move_correct(negras)):
                Partida.variacion.append(negras)

                Motor.set_position(Partida.variacion)

                Partida.n_movimiento += 1
                Partida.n_jugada += 1

                Partida.jugada_correcta = True
                self.guardarPartida('respaldo')
                self.imprimirNegras()

            # Guardar Partida    
            elif negras == '5':
                self.guardarPartida('partida')
                Partida.jugada_correcta = False

            # Deshacer jugada
            elif negras == '4':
                self.deshacer()
                Partida.jugada_correcta = False

            # Opciones
            elif negras == '3':
                self.imprimirOpciones()
                Partida.jugada_correcta = False

            # Reiniciar
            elif negras == '9':
                Partida.salir = True
    
            # Si la jugada es incorrecta (Motor.is_move_correct == False)
            else:
                self.imprimirGenerico('{} incorrecta!'.format(negras))
                Partida.jugada_correcta = False

                self.titilar()

                time.sleep(2)
                


##################               FUNCIONES              #####################

    ### Guardar partida
    def guardarPartida(self, tipo):
        # Crea diccionario con header y arbol (implementar PGN)
        diccionario = dict(header=Partida.header, variacion=Partida.variacion, n_jugada=Partida.n_jugada,
                           n_movimiento=Partida.n_movimiento, evaluacion=Partida.evaluacion,
                           jugada_correcta=Partida.jugada_correcta, color=self.color, pgn=[])

        # Si es con opcion de grabado automatico (tipo=respaldo)
        if tipo == 'respaldo':
            pickle.dump(diccionario, open('juegos/respaldo.gm'.format(tipo), 'wb'))

        # Si no, pregunta donde guardar el juego (tipo=juego):
        else:
            perfiles = ['perfil1', 'perfil2', 'perfil3', 'perfil4']

            #-------------------
            lista_perfiles = ["Perfil 1","Perfil 2", "Perfil 3", "Perfil 4"]
            opcion = self.imprimirGenerico("Guardar en:", "Perfil 1", "Perfil 2",
                                           "Perfil 3", "Perfil 4", seleccion=True)
            
            nombre_archivo = perfiles[int(opcion) - 1]
            nombre_perfil = lista_perfiles
            [int(opcion) - 1]
            
            pickle.dump(diccionario, open('juegos/{}.gm'.format(nombre_archivo), 'wb'))
            
            self.imprimirGenerico("Guardado en", "{}.gm !!".format(nombre_perfil))
            time.sleep(2)


    ### Cargar variacion
    def cargarPartida(self, tipo):

        if tipo == 'respaldo':
            print("respaldo?")
            try:
                diccionario = pickle.load(open('juegos/{}.gm'.format(tipo), 'rb'))
                
                Partida.header          = diccionario['header']
                Partida.variacion           = diccionario['variacion']
                Partida.n_jugada        = diccionario['n_jugada']
                Partida.n_movimiento    = diccionario['n_movimiento']
                Partida.evaluacion      = diccionario['evaluacion']
                Partida.jugada_correcta = diccionario['jugada_correcta']
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

                Partida.header          = diccionario['header']
                Partida.variacion           = diccionario['variacion']
                Partida.n_jugada        = diccionario['n_jugada']
                Partida.n_movimiento    = diccionario['n_movimiento']
                Partida.evaluacion      = diccionario['evaluacion']
                Partida.jugada_correcta = diccionario['jugada_correcta']
                self.color            = diccionario['color']

                self.imprimirGenerico("Partida cargada", "'{}.gm'!!".format(opcion), "Arbol jugadas")
                print('Partida cargado')
                
            except FileNotFoundError:
                self.imprimirGenerico("{}".format(opcion), "no existe...")
                            

        Motor.set_position(Partida.variacion)
        #print(Motor.get_board_visual())
        time.sleep(2)

            
    ### Formatear Partida
    def formatearPartida(self):
        
        if len(Partida.variacion) <= 4:
            Partida.ultimas = Partida.variacion + ["*"] + ([" "] * (3 - len(Partida.variacion)))

        else:
            Partida.ultimas = Partida.variacion[-3:] + ["*"]


    ### Imprimir pantalla para negras            
    def imprimirNegras(self):
        self.formatearPartida()
    
        if Partida.n_jugada == 1:
            line2 = " 1. {} {}".format(Partida.ultimas[0], Partida.ultimas[1])
            line3 = " 2. {} {}".format(Partida.ultimas[2], Partida.ultimas[3])        
        else:
            line2 = " {}. {} {}".format(Partida.n_jugada - 1, Partida.ultimas[0], Partida.ultimas[1])
            line3 = " {}. {} {}".format(Partida.n_jugada - 0, Partida.ultimas[2], Partida.ultimas[3])        


        line1 = " Analisis: {}".format(Partida.evaluacion)
        line4 = " "
        line5 = " "
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
        line2 = "(1) Luz" # Cambiar a que se pueda hacer scroll por el Partida completo
        line3 = "(2) Cargar"
        line4 = "(3) Analisis"
        line5 = "(4) Variante"
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
                    
            elif opcion == '8':
                v -= 1
                if v < 1:
                    v = 5
                    
            ### Volver al Partida
            elif opcion == '4':
                volver = True

            elif opcion == '5':
                if v == 1:
                    self.lcd_on = not self.lcd_on
                    lcd.backlight(self.lcd_on)
                    
                if v == 2:
                    self.cargarPartida('variacion')
                    time.sleep(2)

                else:
                    self.imprimirGenerico("No implementada...")

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
        out = ' '
        
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

                elif opcion == '4':
                    break

                elif opcion == '5':
                    out = v
                    break

            else:
                break

        return out
        

    ### Invertir color de lineas de la pantalla
    def invertirColor(self, opcion, h=1, v=1, vector_inversion=[False, True, False, False, False, False]):

        # ELIMINAR !!
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
        

    def titilar(self):
        lcd.backlight(True)
        time.sleep(0.2)
        lcd.backlight(False)
        time.sleep(0.5)

        lcd.backlight(True)
        time.sleep(0.2)
        lcd.backlight(False)
        time.sleep(0.5)

        lcd.backlight(True)
        time.sleep(0.2)
        lcd.backlight(False)
        time.sleep(1)

        lcd.backlight(True)
    

    ### Deshacer jugada
    def deshacer(self):
        ### Si en el Partida hay mas de 1 jugada:
        if len(Partida.variacion) > 1:
            # Borra las ultimas dos
            del Partida.variacion[-2:]

            # Fija posicion y reevalua
            Motor.set_position(Partida.variacion)
            evaluacion = Motor.get_evaluation()
            Partida.evaluacion = evaluacion['value'] / 100

            Partida.n_jugada     -= 1
            Partida.n_movimiento -= 2

        # Si no hay jugadas suficientes para deshacer    
        else:
            self.imprimirGenerico("No hay mas jugadas", "que deshacer!")
            time.sleep(1)



