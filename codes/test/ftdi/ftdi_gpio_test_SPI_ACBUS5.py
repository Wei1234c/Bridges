from bridges.ftdi.controllers.spi import SpiController
from bridges.interfaces.micropython.machine import Pin


ctrl = SpiController()
machine = ctrl.get_gpio()

print(machine.addressable_pins)
p0 = machine.Pin('ACBUS5', mode = Pin.OUT)

print(p0.value())

p0.value(0)
print(p0.value())

p0.value(1)
print(p0.value())
