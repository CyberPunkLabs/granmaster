import numpy

import Font

    
class Framebuffer:
    def __init__(self):
        self.buffer = numpy.zeros((84, 48), dtype = numpy.int8)


    def clear(self):
        self.buffer = numpy.zeros((84, 48), dtype = numpy.int8)


    def invert(self, x0, y0, x1, y1):
        for x in numpy.arange(x0, x1 + 1):
            for y in numpy.arange(y0, y1 + 1):
                self.buffer[x, y] = int(not bool(self.buffer[x, y]))


    def write(self, xPosition, yPosition, font, text, inverse = False, xDelta = None, yDelta = None):
        if xDelta is None:
            xDelta = int((84 - font.xCharacter * font.width) / 2)

        if yDelta is None:
            yDelta = int((48 - font.yCharacter * font.height) / 2)
        
        if xPosition < font.xCharacter - 1 or yPosition < font.yCharacter - 1:
            for c in text:
                offset = ord(c) * font.width
            
                for x in range(font.width):
                    for y in range(font.height):
                        pixel = font.buffer[offset + x, y]
                        
                        if inverse:
                            pixel = int(not bool(pixel))
                            
                        self.buffer[xDelta + xPosition * font.width + x, yDelta + yPosition * font.height + y] = pixel

                xPosition += 1

                if xPosition == font.xCharacter:
                    xPosition = 0
                    yPosition += 1

                if yPosition == font.yCharacter:
                    return



















