### Importa modulos requieridos por Gran Master
import time
import pickle
import random

#from lcd5110 import LCD5110
from stockfish import Stockfish


### Declara stockfish
Motor = Stockfish("/usr/games/stockfish", parameters={'Contempt': 0, 'MultiPV': 4}) # Mismos valores que default

print("\n\n########### INICIO DEL JUEGO " + "############\n")
print('[CPLs] Parametros de Stockfish:')

### Fija motor en simple, para hacer pruebas
print(Motor.get_parameters())
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
    imprimir_tablero = False
    #lcd_on = True


    ### Pantalla de inicio. Revisar si adecuado declararla en __init__
    def __init__(self):

        ### Despliega pantallas de configuracion
        #self.configuracion()
        self.crearPerfil()



##################       Inicio del loop principal         #####################
    def jugada(self):
        if self.color == 'blancas':
            ### Imprime info (para desarrolladores)
            if Partida.imprimir_tablero:
                print("[CPLs] Tablero:")
                print(Motor.get_board_visual())
            self.imprimirNegras()
            print("[CPLs] Partida: {}".format(Partida.variacion))

            self.HUMANO()
            self.REPLICANTE()
            #print("[CPLs] Jugada correcta? {}".format(Partida.jugada_correcta))

        else:
            #print("[CPLs] Jugada correcta? {}".format(Partida.jugada_correcta))


            self.REPLICANTE()

            ### Imprime info (para desarrolladores)
            if Partida.imprimir_tablero:
                print("[CPLs] Tablero:")
                print(Motor.get_board_visual())
            self.imprimirNegras()
            print("[CPLs] Partida: {}".format(Partida.variacion))

            self.HUMANO()



##################               FUNCIONES              #####################
    def HUMANO(self):
        ### Espera por input de las negras y lo transforma a minusculas (para reconocimiento posterior)
        entrada = input().lower()

        # Si existe input y este es una jugada correcta
        if (len(entrada) > 1) & (Motor.is_move_correct(entrada)):
            Partida.jugada_correcta = True
            Partida.variacion.append(entrada)
            self.evaluarPosicion()

            ### Añade movimiento y jugada (revisar)
            Partida.n_movimiento += 1
            Partida.n_jugada += 1
            #self.guardarPartida('respaldo')
            #self.imprimirNegras()

        else:
            self.manipularOpciones(entrada)

        return entrada


    def REPLICANTE(self):
        if Partida.jugada_correcta:
            self.imprimirGenerico("Replicante {}.{}".format(self.skill, self.depth), "esta pensando...", dwell=1)

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

            self.evaluarPosicion()
            #self.imprimirNegras()

        ### Si la jugada no es correcta, simplementa pasa
        else:
            pass


    def LIBRO(self, entrada):
        if entrada == Partida.apertura[Partida.n_movimiento]:
            self.imprimirGenerico('Jugando', 'apertura...', dwell=1)

            ### Toma jugada de best_move dado nivel y profundidad
            com = Partida.apertura[Partida.n_movimiento]

	    ### Agrega la jugada al arbol de la partida
            Partida.variacion.append(com)
            Partida.n_movimiento += 1
            print("[CPLs] n movimiento: {}".format(Partida.n_movimiento))

            self.evaluarPosicion()
            #self.imprimirNegras()

        ### Si la jugada no es correcta, simplementa pasa
        else:
            pass


    def evaluarPosicion(self):
        ### Mejora habilidad y evalua tablero
        Motor.set_skill_level(20)
        Motor.set_depth(20)

        ### Fija posicion en el tablero
        Motor.set_position(Partida.variacion)
        evaluacion = Motor.get_evaluation()
        Partida.evaluacion = evaluacion #['value'] / 100

        ### Vuelve a habilidad por defecto
        Motor.set_skill_level(self.skill)
        Motor.set_depth(self.depth)

        ### Vuelve a fijar posicion en el tablero
        Motor.set_position(Partida.variacion)
        evaluacion = Motor.get_evaluation()
        Partida.evaluacion = evaluacion #['value'] / 100



    def manipularOpciones(self, entrada):
        if entrada == "1245":
            pass
        elif entrada == "a":
            print("[CPLs] Análisis:")
            Motor.set_skill_level(20)
            Motor.set_depth(20)
            Motor.get_analysis()
            Motor.set_skill_level(self.skill)
            Motor.set_depth(self.depth)
            print("\n")
            #self.imprimirNegras()
        elif entrada == "f":
            print("[CPLs] FEN position:")
            print(Motor.get_fen_position())
            print("\n")
        elif entrada == "d":
            self.deshacer()
        elif entrada == "e":
            self.escribirPartida(tipo='juego')
        elif entrada == "t":
            print("[CPLs] Tablero:")
            print(Motor.get_board_visual())
        # Si la jugada es incorrecta (Motor.is_move_correct == False ??)
        else:
            self.imprimirGenerico("{} incorrecta!".format(entrada), "s: Analisis", "t: tablero",
                                  "f: Posicion FEN", "d: deshacer", "e: escribir juego", dwell=2)
            #self.titilar()
        Partida.jugada_correcta = False


    ### Deshacer jugada
    def deshacer(self):
        Partida.jugada_correcta = False

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

        # Si no hay jugadas suficientes para deshacer
        else:
            self.imprimirGenerico("No hay mas jugadas", "que deshacer!", dwell=2)

        self.imprimirNegras()


    ### Imprimir pantalla para negras
    def imprimirNegras(self):
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
                Motor.set_skill_level(self.skill)
                self.imprimirGenerico('Replicante', 'Skill level: {}.'.format(self.skill), dwell=1)
                break
            else:
                self.imprimirGenerico('Opción incorrecta!', dwell=2)


        ### Version replicante (profundidad jugada)
        while True:
            self.imprimirGenerico('Depth','(0-20)')
            opcion = input()
            try:
                self.depth = int(opcion)
            except ValueError:
                self.imprimirGenerico('Opción incorrecta!', dwell=1)
                continue
            if (self.depth >= 0) & (self.depth <= 20):
                Motor.set_depth(self.depth)
                self.imprimirGenerico('Replicante', 'Depth {}.'.format(self.depth), dwell=1)
                break
            else:
                self.imprimirGenerico('Opción incorrecta!', dwell=1)


        ### Color del jugador
        while True:
            self.imprimirGenerico('Color', '(1) Blancas', '(2) Negras', '(3) Aleatorio', '(4) Hum vs Hum', '(5) Rep vs Rep')
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

                self.imprimirGenerico('Color', '{}.'.format(self.color), dwell=2)
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
                    self.configuracion()

                self.imprimirGenerico('Color', '{}.'.format(self.color), dwell=2)
                break

            else:
                self.imprimirGenerico('Opción incorrecta!', dwell=2)


#################
    ### Guardar juego
    def escribirPartida(self, tipo):
        # Crea diccionario con header y arbol (implementar PGN)
        diccionario = dict(header=Partida.header, variacion=Partida.variacion, n_jugada=Partida.n_jugada,
                           n_movimiento=Partida.n_movimiento, evaluacion=Partida.evaluacion,
                           jugada_correcta=Partida.jugada_correcta, color=self.color, pgn=[])

        # Si es con opcion de grabado automatico (respaldo)
        if tipo == 'respaldo':
            pickle.dump(diccionario, open('juegos/{}.gm'.format(tipo), 'wb'))

        # Si no, pregunta donde guardar el juego:
        else:
            perfiles = ['perfil1', 'perfil2', 'perfil3', 'perfil4', 'perfil5']

            #-------------------  
            self.imprimirGenerico("Selecciona:", "(1) Perfil", "(2) Perfil",
                                  "(3) Perfil", "(4) Perfil", "(5) Perfil")


            opcion = input()
            opcion = perfiles[int(opcion) - 1]

            pickle.dump(diccionario, open('juegos/{}.gm'.format(opcion), 'wb'))

            self.imprimirGenerico("Guardado en", "{}.gm !!".format(opcion))
            time.sleep(2)


   ### Cargar juego
    def leerPartida(self, tipo):

        if tipo == 'respaldo':
            try:
                diccionario = pickle.load(open('juegos/{}.gm'.format(tipo), 'rb'))

                Partida.header          = diccionario['header']
                Partida.variacion       = diccionario['variacion']
                Partida.n_jugada        = diccionario['n_jugada']
                Partida.n_movimiento    = diccionario['n_movimiento']
                Partida.evaluacion      = diccionario['evaluacion']
                Partida.jugada_correcta = diccionario['jugada_correcta']
                self.color              = diccionario['color']

            except FileNotFoundError:
                self.imprimirGenerico("respaldo.gm", "no existe...")


        else:
            perfiles = ['perfil1', 'perfil2', 'perfil3', 'perfil4', 'perfil5']

            #-------------------  
            self.imprimirGenerico("Selecciona:", "(1) Perfil", "(2) Perfil",
                                  "(3) Perfil", "(4) Perfil", "(5) Perfil")


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

                self.imprimirGenerico("Perfil cargado", "{} !!".format(opcion))

            except FileNotFoundError:
                self.imprimirGenerico("{}".format(opcion), "no existe...")


        Motor.set_position(Partida.variacion)
        #print(stockfish.get_board_visual())
        time.sleep(2)




