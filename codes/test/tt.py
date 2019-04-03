import os
import sys
sys.path.append(os.path.abspath(os.path.join('..', )))


from bridges.ftdi.controllers.gpio import GpioController
from bridges.interfaces.micropython.machine import Pin


ctrl = GpioController()
# ctrl = GpioController(product = 'ft2232h', interface = 2)
pin_out = ctrl.Pin('ADBUS6', mode = Pin.OUT)



def blinks(pin):
    from time import sleep

    def blink(delay = 0.2):
        pin.toggle()
        sleep(delay)
        pin.toggle()
        sleep(delay)


    for i in range(3):
        print(i)
        blink()



blinks(pin_out)

ctrl.terminate()
