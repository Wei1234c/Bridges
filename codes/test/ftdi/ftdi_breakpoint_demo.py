from bridges.ftdi.controllers.gpio import GpioController
from bridges.interfaces.micropython.machine import Pin

machine = GpioController()


pin = machine.Pin(6, mode = Pin.OUT)
i = 0
while True:
    i+=1
    pin.value(1)
    pin.value(0)
    print(i)


ctrl.terminate()
