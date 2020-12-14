
        
###################################################        
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
            
                self.imprimirGenerico("Jugando", "{}".format(Partida.nombre_apertura.title()))

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

