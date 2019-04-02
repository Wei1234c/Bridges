import bridges.interfaces.micropython.machine as I_machine
from bridges.ftdi.controllers.gpio import GpioController


ctrl1 = GpioController(product = 'ft2232h', interface = 1)

ctrl2 = GpioController(product = 'ft2232h', interface = 2)

pin1 = ctrl1.Pin('ADBUS6', mode = I_machine.Pin.OUT)
pin2 = ctrl2.Pin('BDBUS6', mode = I_machine.Pin.OUT)



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



blinks(pin1)
blinks(pin2)

ctrl1.terminate()
ctrl2.terminate()
