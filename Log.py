import numpy

import Lcd
import Framebuffer
import Font
import Keys


class Log:
    def __init__(self, font):
        self.font = font
        self.framebuffer = Framebuffer.Framebuffer()
        self.log = []


    def clear(self):
        self.log.clear()


    def append(self, text):
        while len(text) > 0:
            slice = text[:self.font.xCharacter]
            text = text[self.font.xCharacter:]
            
            self.log.append(slice)

        self.log = self.log[-self.font.yCharacter:]


    def render(self):
        self.framebuffer.clear()

        for i in range(len(self.log)):
            self.framebuffer.write(0, i, self.font, self.log[i])

        return self.framebuffer

