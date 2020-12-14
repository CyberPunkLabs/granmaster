import numpy

import Lcd
import Framebuffer
import Font
import Keys


class Menu:
    def __init__(self, lcd, keyEvent, font, lines, options, selection, left = True):
        self.lcd = lcd
        self.keyEvent = keyEvent
        self.font = font
        self.lines = lines
        self.options = options
        self.selection = selection
        
        self.framebuffer = Framebuffer.Framebuffer()

        if left:
            self.xDelta = 0 
        else:
            self.xDelta = int((font.xCharacter - max([len(x) + 1 for x in options])) / 2)
        self.yDelta = int((font.yCharacter - len(self.options)) / 2)


    def run(self):
        while True:
            self.framebuffer.clear()

            for i in range(len(self.lines)):
                row = self.lines[i]

                if i > 3: 
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

            self.selection %= len(self.lines)

            if pressed == 'enter':
                return self.selection
