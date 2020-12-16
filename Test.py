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

font = Font.Font('FONTS\Incomplete.F08')

log = Log.Log(font)


menuRows = ['Elegir', '', 'Jugar', 'Rendirse', 'Salir', 'Ayuda']
#move = Move.Move(lcd, keyEvent, font)
menu = Menu.Menu(lcd, keyEvent, font, menuRows, [2, 3, 4, 5], 3)

selection = menu.run()
print(selection)

#log.append('Opcion: {:s}'.format(menuOptions[selection]))
#lcd.update(log.render())
#pyplot.pause(2)

# selection = move.run()
# log.append('Jugada: {:s}'.format(selection))
# lcd.update(log.render())
# pyplot.pause(2)

# for i in range(10):
#     log.append('Line {:d}'.format(i))
#     lcd.update(log.render())
#     pyplot.pause(1)
