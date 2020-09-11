import numpy

import Lcd
import Framebuffer
import Font
import Keys


class Move:
    def __init__(self, lcd, keyEvent, font, title = 'Move:', move = 'A1A1'):
        self.lcd = lcd
        self.keyEvent = keyEvent
        self.font = font
        self.title = title
        self.move = move
        
        self.framebuffer = Framebuffer.Framebuffer()

        self.cursor = 0
        
        self.xDelta = int((font.xCharacter - max(len(self.title), 7)) / 2)

                            
    def __updateMove(self, delta):
        moveList = list(self.move)

        if self.cursor  % 2 == 0:
            moveList[self.cursor] = chr((ord(moveList[self.cursor]) - ord('A') + delta) % 8 + ord('A'))
        else:
            moveList[self.cursor] = chr((ord(moveList[self.cursor]) - ord('1') + delta) % 8 + ord('1'))

        self.move = ''.join(moveList)


    def run(self):
        while True:
            self.framebuffer.clear()

            moveString = self.move[0 : 2] + ' - ' + self.move[2 : 4]
            
            if self.cursor < 2:
                cursorString = ' ' * self.cursor + '^'
            else:
                cursorString = '   ' + ' ' * self.cursor + '^'

            self.framebuffer.write(self.xDelta, 1, self.font, self.title)
            self.framebuffer.write(self.xDelta, 3, self.font, moveString)
            self.framebuffer.write(self.xDelta, 4, self.font, cursorString)
            
            while True:
                pressed = self.keyEvent.get()
                self.lcd.update(self.framebuffer)

                if pressed == 'up' or pressed == 'down' or pressed == 'left' or pressed == 'right' or pressed == 'enter':
                    break

            if pressed == 'up':
                self.__updateMove(1)

            if pressed == 'down':
                self.__updateMove(-1)

            if pressed == 'left':
                self.cursor -= 1
                self.cursor %= 4

            if pressed == 'right':
                self.cursor += 1
                self.cursor %= 4

            if pressed == 'enter':
                return self.move

