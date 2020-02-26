import machine
import unified
# from bridges.tools import unified

pin_id = 2
pin = machine.Pin(pin_id, machine.Pin.OUT)

id = 1
spi = machine.SPI(id, baudrate = 10000000, polarity = 0, phase = 0)
spi.init()

# pin = None
spi = unified.SPI.from_uPy(spi, pin_ss = pin)

spi.transfer(address = 3, value = 0x00)
