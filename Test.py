import os
import matplotlib.pyplot as pyplot

import Keys
import Lcd
import Framebuffer
import Font
import Menu
import Log
import Move

# Soluciona problema X display en Unix
if os.name == 'nt':
    pass
else: 
    os.system("xhost si:localuser:root")

    
lcd = Lcd.Lcd()
keyEvent = Keys.KeyEvent()

font = Font.Font('FONTS/BIGPILE/SEEMORE/CM-6X8.F08')

log = Log.Log(font)


menuOptions = ['Jugar', 'Rendirse', 'Salir', 'Ayuda', '1', '2']
move = Move.Move(lcd, keyEvent, font)
menu = Menu.Menu(lcd, keyEvent, font, menuOptions, 2)


# selection = menu.run()
# log.append('Opcion: {:s}'.format(menuOptions[selection]))
# lcd.update(log.render())
# pyplot.pause(2)

selection = move.run()
log.append('Jugada: {:s}'.format(selection))
lcd.update(log.render())
pyplot.pause(2)

# for i in range(10):
#     log.append('Line {:d}'.format(i))
#     lcd.update(log.render())
#     pyplot.pause(1)
