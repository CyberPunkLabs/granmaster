import numpy
import matplotlib.pyplot as pyplot


try:
    import RPi.GPIO as gpio
    raspberryPi = True
except (ImportError, RuntimeError):
    import matplotlib.pyplot as pyplot
    raspberryPi = False


class Lcd:
    def __init__(self):
        if raspberryPi:
            print('TODO!')
        else:
            # [ERROR] Solucionado con xhost si:localuser:root            
            self.fig, self.ax = pyplot.subplots(1, 1)
            #
            
            self.im = self.ax.imshow(numpy.zeros((48, 84), dtype = numpy.int8), aspect = 'equal', vmin = 0, vmax = 1)



    def update(self, framebuffer):
        if raspberryPi:
            print('TODO!')
        else:
            self.im.set_data(framebuffer.buffer.T)
            self.fig.canvas.draw_idle()
            pyplot.pause(.01)

