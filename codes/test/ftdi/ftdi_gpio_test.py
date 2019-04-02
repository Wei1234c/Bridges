from bridges.ftdi.controllers.gpio import GpioController


ctrl = GpioController()
# ctrl = GpioController(product = 'ft2232h', interface = 2)
print(ctrl.addressable_pins)
import bridges.interfaces.micropython.machine as I_machine
from bridges.interfaces.micropython.machine import Pin

pin_in = ctrl.Pin('ADBUS5', mode = Pin.IN)
pin_out = ctrl.Pin('ADBUS6', mode = Pin.OUT)
# pin_in = ctrl.Pin('BDBUS5', mode = I_machine.Pin.IN)
# pin_out = ctrl.Pin('BDBUS6', mode = I_machine.Pin.OUT)

print(ctrl.pins_values)
print(ctrl.pins_values_list)

print('pin_in:', pin_in())



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
