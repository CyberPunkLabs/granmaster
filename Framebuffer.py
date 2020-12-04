import numpy

import Font

    
class Framebuffer:
    def __init__(self):
        self.buffer = numpy.zeros((84, 48), dtype = numpy.int8)


    def clear(self):
        self.buffer = numpy.zeros((84, 48), dtype = numpy.int8)


    def invert(self):
        for x in range(84):
            for y in range(48):
                self.buffer[x, y] = pixel = int(not bool(self.buffer[x, y]))


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



















