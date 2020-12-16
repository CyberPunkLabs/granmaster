import numpy
import matplotlib.pyplot as pyplot
import os
import glob
import Font

path = 'FONTS'

for filename in glob.iglob(path + '/**/*.F*', recursive=True):
    #f = Font.font(file)

    height = int(filename[-2:])
    width = 8

    with open(filename, 'rb') as file:
        binary = list(file.read())

    row = 0
    for r in binary:
        row |= r

    while (row & 1 == 0):
        width -= 1
        row >>= 1

    xCharacter = int(84 / width)
    yCharacter = int(48 / height) 

    buffer = numpy.zeros((256 * width, height), dtype = numpy.int8)

    for column in range(256):
        for y in range(height):
            for x in range(width):
                buffer[column * width + x, y] = (binary[column * height + y] >> 7 - x) & 1

    print(xCharacter, yCharacter, filename)


