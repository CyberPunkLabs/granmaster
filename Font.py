import re
import numpy
import matplotlib.pyplot as pyplot


class Font:
    def __init__(self, filename):
        self.height = int(filename[-2:])
        self.width = 8

        with open(filename, 'rb') as file:
            binary = list(file.read())

        row = 0
        for r in binary:
            row |= r

        while (row & 1 == 0):
            self.width -= 1
            row >>= 1

        self.xCharacter = int(84 / self.width)
        self.yCharacter = int(48 / self.height) 

        self.buffer = numpy.zeros((256 * self.width, self.height), dtype = numpy.int8)

        for column in range(256):
            for y in range(self.height):
                for x in range(self.width):
                    self.buffer[column * self.width + x, y] = (binary[column * self.height + y] >> 7 - x) & 1
