#!/usr/bin/env python3

### Pip
# pip3 install keyboard
# pip3 install stockfish


# Modules
#import time
#import random
#import pickle
#import keyboard

from CyberPunkChess_testing import Juego

#opcion = input('Cargar juego? (s/n): ')

juego = Juego()

salir = False
while not salir:
    juego.jugada()

    salir = juego.salir
