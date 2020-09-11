import time

try:
    import RPi.GPIO as gpio
    raspberryPi = True
except (ImportError, RuntimeError):
    import keyboard
    raspberryPi = False


def state(key):
    key = key.lower()
    
    if raspberryPi:
        print('TODO!')
    else:
        if key == 'up':
            return keyboard.is_pressed('up')
        elif key == 'down':
            return keyboard.is_pressed('down')
        elif key == 'left':
            return keyboard.is_pressed('left')
        elif key == 'right':
            return keyboard.is_pressed('right')
        elif key == 'enter':
            return keyboard.is_pressed('enter')
        else:
            return None


class KeyEvent:
    def __init__(self, scanPeriod = 0.05):
        self.scanPeriod = scanPeriod
        
        self.up    = state('up')
        self.down  = state('down')
        self.left  = state('left')
        self.right = state('right')
        self.enter = state('enter')

        self.t = time.time()


    def get(self):
        event = None

        t = time.time()
        
        if t - self.t > self.scanPeriod:
            up    = state('up')
            down  = state('down')
            left  = state('left')
            right = state('right')
            enter = state('enter')

            if self.up == False and up == True:
                event = 'up'
            
            if self.down == False and down == True:
                event = 'down'

            if self.left == False and left == True:
                event = 'left'

            if self.right == False and right == True:
                event = 'right'

            if self.enter == False and enter == True:
                event = 'enter'

            self.up    = up
            self.down  = down
            self.left  = left
            self.right = right
            self.enter = enter

            self.t = t

        return event
