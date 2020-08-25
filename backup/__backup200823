### Importa modulos requieridos por Gran Master
import time
import pickle
import random

#from lcd5110 import LCD5110
from stockfish import Stockfish


### Declara stockfish y control sobre pantalla LCD
Motor = Stockfish("/usr/games/stockfish", parameters={'Contempt': 0})

print("\n\n########### INICIO DEL JUEGO " + "############\n")
print('Parametros de Stockfish:')
print(Motor.get_parameters())
#lcd = LCD5110()


### Clase principal
class Partida:

    ''' Llama a stockfish y efectua e imprime la jugada.

[Historial]

[Pendientes]
-> Auditar la evaluacion de la jugada. Intentar actualizarla cada ej 3 s 
-> Traducir a ELO
-> Entrenador de aperturas
-> Que seleccione dificultad Stockfish segun ELO participante
-> Introducir scroll por partida
-> Introducir variantes

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
    aperturas = pickle.load(open('basesdatos/libroAperturas.gm', 'rb'))
    variacion = []
    n_movimiento = 0
    n_jugada = 1
    jugada_correcta = True
    salir = False
    #lcd_on = True


    
    ### Pantalla de inicio. Revisar si adecuado declararla en __init__
    def __init__(self):

        line2 = "#" * 17
        line3 = "#  Bienvenido   " + "#"
        line4 = "#     v.0.1     " + "#"
        line5 = "#" * 17

        ### Despliega pantallas de configuracion
        #self.configuracion()           
        self.color = 'n'

        #time.sleep(0.2)
        #lcd.backlight(False)
        #time.sleep(0.5)
        self.imprimirGenerico(line2=line2, line3=line3, line4=line4, line5=line5, seleccion=False, dwell=2)
        #self.titilar()

        ### Banco o partida
        while True:
            opcion = input("Tipo (1) Partida (2) Banco: ")
	    
            if opcion == '1':
                Partida.tipo = 'juego'
                break
            elif opcion == '2':
                Partida.tipo = 'banco'

                Partida.nombre_apertura = random.choice(list(Partida.aperturas.keys()))
                Partida.apertura = Partida.aperturas[Partida.nombre_apertura]

                break
            else:
                print('Opcion incorrecta!')

                
##################       Inicio del loop principal         #####################
    def jugada(self):
        ### Para las blancas ###
        if self.color == 'b':
            pass

        
        ### Para las negras ###
        else:

            ### Si la jugada anterior de las negras es correcta:
            if Partida.jugada_correcta:
                if Partida.tipo == 'juego':
                    self.imprimirGenerico('Replicante 0.1', 'esta pensando...', dwell=1)

                    if Partida.n_jugada == 1:
                        blancas = random.choice(Partida.aperturas['top10'])

                    ### Si la jugada es > 1, juega Stockfish
                    else:
                        clock = time.time()

                        ### Toma jugada de best_move dado nivel y profundidad
                        blancas = Motor.get_best_move()
                        ### Alternativamente, podria tomarla de best_move_time dado limite temporal
                        #blancas = Motor.get_best_move_time(2000)
                        print('Jugada en {} s.'.format(time.time() - clock))


                elif Partida.tipo == 'banco':
                    #nombre = random.choice(list(Partida.aperturas.keys()))
                    #apertura = aperturas[nombre]

                    self.imprimirGenerico('Jugando:', '{}'.format(Partida.nombre_apertura), dwell=2)
                    print("[CPLS] {}: {}".format(Partida.nombre_apertura, Partida.apertura))
                    blancas = Partida.apertura[Partida.n_movimiento]


                ### Agrega la jugada al arbol de la partida
                Partida.variacion.append(blancas)
                Partida.n_movimiento += 1
                print("[CPLs] n movimiento: {}".format(Partida.n_movimiento))


                ### Fija posicion en el tablero y evalua la posicion
                Motor.set_position(Partida.variacion)
                evaluacion = Motor.get_evaluation()
                Partida.evaluacion = evaluacion['value'] / 100


            ### Imprime info
            self.imprimirNegras()
            print("[CPLs] Tablero:")
            print(Motor.get_board_visual())


            if (Partida.tipo == 'banco') & (Partida.n_movimiento == len(Partida.apertura)):
                self.imprimirGenerico("Variacion terminada!", dwell=2)
                Partida.salir = True


            ### Espera por input de las negras y lo transforma a minusculas (para reconocimiento posterior)
            negras = input().lower()

            if Partida.tipo == 'juego':
                if (len(negras) > 1) & (Motor.is_move_correct(negras)):
                    Partida.jugada_correcta = True

            # Para banco
            else:
                if (len(negras) > 1) & (negras == Partida.apertura[Partida.n_movimiento]):
                    Partida.jugada_correcta = True
                else:
                    self.imprimirGenerico(negras, "incorrecta...", dwell=2)
                    Partida.jugada_correcta = False


            ### Respuestas al input
            # Si existe input y este es una jugada correcta
            if Partida.jugada_correcta:
                Partida.variacion.append(negras)

                Motor.set_position(Partida.variacion)

                Partida.n_movimiento += 1
                Partida.n_jugada += 1


                #if Partida.n_movimiento == len(Partida.aperturas['ruy-lopez']):
                #    self.imprimirGenerico("Variacion terminada!", dwell=2)
                #    Partida.salir = True


                #self.guardarPartida('respaldo')
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

                #self.titilar()

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
            self.imprimirGenerico("Guardar en:", "Perfil 1", "Perfil 2",
                                           "Perfil 3", "Perfil 4", seleccion=True)
            
            opcion = input()
            nombre_archivo = perfiles[int(opcion) - 1]
            nombre_perfil = lista_perfiles[int(opcion) - 1]
            
            pickle.dump(diccionario, open('juegos/{}.gm'.format(nombre_archivo), 'wb'))
            
            self.imprimirGenerico("Guardado en", "{}.gm !!".format(nombre_perfil))
            time.sleep(2)


    ### Cargar variacion
    def cargarPartida(self, tipo):

        if tipo == 'respaldo':
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
            perfiles = ['perfil1', 'perfil2', 'perfil3', 'perfil4']

            #-------------------  
            self.imprimirGenerico("Cargar perfil:", "Perfil 1", "Perfil 2",
                                  "Perfil 3", "Perfil 4", seleccion=False, dwell=2)
            
            opcion = input()
            opcion = perfiles[int(opcion) - 1]

            try:
                diccionario = pickle.load(open('juegos/{}.gm'.format(opcion), 'rb'))

                Partida.header          = diccionario['header']
                Partida.variacion       = diccionario['variacion']
                Partida.n_jugada        = diccionario['n_jugada']
                Partida.n_movimiento    = diccionario['n_movimiento']
                Partida.evaluacion      = diccionario['evaluacion']
                Partida.jugada_correcta = diccionario['jugada_correcta']
                self.color              = diccionario['color']

                self.imprimirGenerico("Partida cargada", "'{}.gm'!!".format(opcion), "Arbol jugadas", dwell=2)

                
            except FileNotFoundError:
                self.imprimirGenerico("{}".format(opcion), "no existe...", dwell=2)
                            
        Motor.set_position(Partida.variacion)
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

        self.imprimirGenerico(line1, line2, line3, line4, line5, line6, seleccion=False)


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

        self.imprimirGenerico(line1, line2, line3, line4, line5, line6, seleccion=False)


    ### Imprimir generico
    def imprimirGenerico(self, line1=" ", line2=" ", line3=" ", line4=" ", line5=" ", line6=" ", seleccion=False, dwell=1):
        print("\n########### PANTALLA DEL USUARIO " + "############")
        print("{}\n{}\n{}\n{}\n{}\n{}\n".format(line1, line2, line3, line4, line5, line6))
        print("########### FIN PANTALLA DEL USUARIO " + "############\n")

        time.sleep(dwell)
        

    ### Deshacer jugada
    def deshacer(self):
        ### Si la partida tiene mas de 1 movimiento:
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



