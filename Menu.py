import numpy

import Lcd
import Framebuffer
import Font
import Keys


class Menu:
    def __init__(self, lcd, keyEvent, font, options, selection):
        self.lcd = lcd
        self.keyEvent = keyEvent
        self.font = font
        self.options = options
        self.selection = selection
        
        self.framebuffer = Framebuffer.Framebuffer()

        self.xDelta = int((font.xCharacter - max([len(x) + 1 for x in options])) / 2)
        self.yDelta = int((font.yCharacter - len(self.options)) / 2)


    def run(self):
        while True:
            self.framebuffer.clear()

            for i in range(len(self.options)):
                row = self.options[i]

                if self.selection == i:
                    row = '>' + row
                else:
                    row = ' ' + row

                self.framebuffer.write(self.xDelta, i + self.yDelta, self.font, row)

            while True:
                pressed = self.keyEvent.get()
                self.lcd.update(self.framebuffer)

                if pressed == 'up' or pressed == 'down' or pressed == 'enter':
                    break

            if pressed == 'up':
                self.selection -= 1

            if pressed == 'down':
                self.selection += 1

            self.selection %= len(self.options)

            if pressed == 'enter':
                return self.selection
