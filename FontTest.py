import numpy
import matplotlib.pyplot as pyplot

import Font


f0 = Font.Font('FONTS\Incomplete.F08')
f1 = Font.Font('FONTS\BIGPILE\SEEMORE\CM-6X8.F08')


print(f0.buffer.shape)
print(f1.buffer.shape)

z = numpy.zeros((f0.buffer.shape[0], 100))

b = numpy.concatenate((z, f0.buffer, f1.buffer, z), 1)

pyplot.imshow(b.T)
pyplot.show()

def test(filename):
    height = int(filename[-2:])
    width = 8

    with open(filename, 'rb') as file:
        binary = list(file.read())

    row = 0
    for r in binary:
        row |= r

    print("{:08b}".format(row))

    while (row & 1 == 0):
        width -= 1
        row >>= 1

    print("{:08b}".format(row))
    print(width)

test('FONTS\Incomplete.F08')
test('FONTS\BIGPILE\SEEMORE\CM-6X8.F08')
