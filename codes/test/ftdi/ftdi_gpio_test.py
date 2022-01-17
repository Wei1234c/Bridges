# from bridges.ftdi.controllers.gpio import GpioAsyncController as GpioController
# from bridges.ftdi.controllers.gpio import GpioSyncController as GpioController
from bridges.ftdi.controllers.gpio import GpioMpsseController as GpioController
from bridges.interfaces.micropython.machine import Pin


machine = GpioController()
# machine = GpioController(product = 'ft2232h', interface = 2)
print(machine.addressable_pins)

# p0 = machine.Pin('ACBUS5', mode = Pin.OUT)
pin_in = machine.Pin('ADBUS5', mode = Pin.IN)
pin_out = machine.Pin('ADBUS6', mode = Pin.OUT)
# pin_in = machine.Pin('BDBUS5', mode = I_machine.Pin.IN)
# pin_out = machine.Pin('BDBUS6', mode = I_machine.Pin.OUT)

print(machine.pins_values)
print(machine.pins_values_list)

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

machine.terminate()
