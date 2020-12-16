import numpy

import Lcd
import Framebuffer
import Font
import Keys


class Menu:
    def __init__(self, lcd, keyEvent, font, rows, options, selection, left = True):
        self.lcd = lcd
        self.keyEvent = keyEvent
        self.font = font
        self.rows = rows
        self.options = options
        self.selection = selection
        
        self.framebuffer = Framebuffer.Framebuffer()

        if left:
            self.xDelta = 0 
        else:
            self.xDelta = int((font.xCharacter - max([len(x) + 1 for x in rows])) / 2)
        self.yDelta = int((font.yCharacter - len(self.rows)) / 2)


    def run(self):
        while True:
            self.framebuffer.clear()

            for i in range(len(self.rows)):
                self.framebuffer.write(self.xDelta, i + self.yDelta, self.font, self.rows[i])
            
            self.framebuffer.invert(0, self.font.height * self.selection, 83, self.font.height * (self.selection + 1) - 1)

            while True:
                pressed = self.keyEvent.get()
                self.lcd.update(self.framebuffer)

                if pressed == 'up' or pressed == 'down' or pressed == 'enter':
                    break

            if pressed == 'up':
                while True:    
                    self.selection = (self.selection - 1) % len(self.rows)
                    if self.selection in self.options:
                        break


            if pressed == 'down':
                while True:
                    self.selection = (self.selection + 1) % len(self.rows)
                    if self.selection in self.options:
                        break

            if (pressed == 'enter'):
                return self.selection

