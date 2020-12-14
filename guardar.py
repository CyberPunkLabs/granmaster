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
            info = ["No perfil", "Guarda juego nuevo"]

            menu = Menu.Menu(lcd, keyEvent, font, info, 0)
            menu.run()
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
                self.imprimirGenerico("El perfil {}".format(opcion), "No existe!")
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
                self.imprimirGenerico("La opción {}".format(opcion), "Es incorrecta.")
                self.crearPerfil()

            TYRELL.set_position(Partida.variacion)
            #print(stockfish.get_board_visual())
            #time.sleep(2)

