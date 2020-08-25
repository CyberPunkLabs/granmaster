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

        ### Despliega pantallas de configuracion
        #self.configuracion()           
        self.color = 'n'

                
##################       Inicio del loop principal         #####################
    def jugada(self):
        print("Correcta? {}".format(Partida.jugada_correcta))

        ### Si la jugada anterior de las negras es correcta:
        self.COM()

        ### Imprime info
        print("[CPLs] Tablero:")
        print(Motor.get_board_visual())
        print("[CPLs] Partida: {}".format(Partida.variacion))


        ### Respuestas al input
        self.HUM()
        
                

##################               FUNCIONES              #####################

    def HUM(self):
        ### Espera por input de las negras y lo transforma a minusculas (para reconocimiento posterior)
        negras = input().lower()
    
        # Si existe input y este es una jugada correcta
        if (len(negras) > 1) & (Motor.is_move_correct(negras)):
            Partida.jugada_correcta = True
            Partida.variacion.append(negras)

            Motor.set_position(Partida.variacion)
            Partida.n_movimiento += 1
            Partida.n_jugada += 1
            #self.guardarPartida('respaldo')
            self.imprimirNegras()

        else:
            self.manipularOpciones(negras)        


    def COM(self):
        if Partida.jugada_correcta:
        
            self.imprimirGenerico('Replicante 0.1', 'esta pensando...', dwell=1)

            if Partida.n_jugada == 1:
                com = random.choice(Partida.aperturas['top10'])

            ### Si la jugada es > 1, juega Stockfish
            else:
                clock = time.time()

                ### Toma jugada de best_move dado nivel y profundidad
                com = Motor.get_best_move()
                ### Alternativamente, podria tomarla de best_move_time dado limite temporal
                #blancas = Motor.get_best_move_time(2000)
                print("[CPLs] Jugada en {} s.".format(time.time() - clock))


	    ### Agrega la jugada al arbol de la partida
            Partida.variacion.append(com)
            Partida.n_movimiento += 1
            print("[CPLs] n movimiento: {}".format(Partida.n_movimiento))

            ### Fija posicion en el tablero y evalua la posicion
            Motor.set_position(Partida.variacion)
            evaluacion = Motor.get_evaluation()
            Partida.evaluacion = evaluacion #['value'] / 100
            
            self.imprimirNegras()



    def manipularOpciones(self, negras):
        if negras == "1245":
           Partida.jugada_correcta = False
        
        elif negras == "4":
            self.deshacer()
            Partida.jugada_correcta = False

        # Si la jugada es incorrecta (Motor.is_move_correct == False)
        else:
            self.imprimirGenerico('{} incorrecta!'.format(negras))
            Partida.jugada_correcta = False

            #self.titilar()

            time.sleep(2)
            



    ### Deshacer jugada
    def deshacer(self):
        ### Si la partida tiene mas de 1 movimiento:
        if len(Partida.variacion) > 2:
            # Borra las ultimas dos
            del Partida.variacion[-2:]

            # Fija posicion y reevalua
            Motor.set_position(Partida.variacion)
            evaluacion = Motor.get_evaluation()
            Partida.evaluacion = evaluacion #['value'] / 100

            Partida.n_jugada     -= 1
            Partida.n_movimiento -= 2
            
            Partida.jugada_correcta = False

        # Si no hay jugadas suficientes para deshacer    
        else:
            self.imprimirGenerico("No hay mas jugadas", "que deshacer!")
            Partida.jugada_correcta = False
            
            time.sleep(1)


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



    ### Imprimir generico
    def imprimirGenerico(self, line1=" ", line2=" ", line3=" ", line4=" ", line5=" ", line6=" ", seleccion=False, dwell=1):
        print("\n########### PANTALLA DEL USUARIO " + "############")
        print("{}\n{}\n{}\n{}\n{}\n{}\n".format(line1, line2, line3, line4, line5, line6))
        print("########### FIN PANTALLA DEL USUARIO " + "############\n")

        time.sleep(dwell)
        


    ### Formatear Partida
    def formatearPartida(self):
        
        if len(Partida.variacion) <= 4:
            Partida.ultimas = Partida.variacion + ["*"] + ([" "] * (3 - len(Partida.variacion)))

        else:
            Partida.ultimas = Partida.variacion[-3:] + ["*"]

