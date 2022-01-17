# from bridges.ftdi.controllers.gpio import GpioAsyncController as GpioController
# from bridges.ftdi.controllers.gpio import GpioSyncController as GpioController
from bridges.ftdi.controllers.gpio import GpioMpsseController as GpioController
from bridges.interfaces.micropython.machine import Pin


machine = GpioController()
print(machine.addressable_pins)

pin_out = machine.Pin('ADBUS5', mode = Pin.OUT)
# pin_out = machine.Pin('ACBUS5', mode = Pin.OUT)

print(machine.pins_values)
print(machine.pins_values_list)



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

machine.terminate()
