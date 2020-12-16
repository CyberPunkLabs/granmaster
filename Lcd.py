import numpy
import lcd5110


try:
    import RPi.GPIO as gpio
    raspberryPi = True
except (ImportError, RuntimeError):
    import matplotlib.pyplot as pyplot
    raspberryPi = False


class Lcd:
    def __init__(self):
        if raspberryPi:
            self.lcd5110 = LCD5110

        else:
            # [ERROR] Solucionado con xhost si:localuser:root            
            self.fig, self.ax = pyplot.subplots(1, 1)
            #
            
            self.im = self.ax.imshow(numpy.zeros((48, 84), dtype = numpy.int8), aspect = 'equal', vmin = 0, vmax = 1)



    def update(self, framebuffer):
        if raspberryPi:
            image = numpy.array((84 * 48) >> 3, dtype = numpy.uint8)
            
            for i in range(framebuffer.buffer >> 3):
                offset = i << 3
                
                for j in range(8):
                    image = framebuffer.buffer[offset + j] << j

            printImage(self, image)

        else:
            self.im.set_data(framebuffer.buffer.T)
            self.fig.canvas.draw_idle()
            pyplot.pause(.01)

