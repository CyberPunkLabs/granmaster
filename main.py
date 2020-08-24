#!/usr/bin/env python3

### Pip
# pip3 install keyboard
# pip3 install stockfish


# Modules
import os
#import time
#import random
#import pickle
#import keyboard

from GranMaster import Partida
#opcion = input('Cargar juego? (s/n): ')

variacion = Partida()

reiniciar = False
while not reiniciar:
    variacion.jugada()

    reiniciar = variacion.salir
    #os.system('python3 main.py')
