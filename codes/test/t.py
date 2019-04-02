# For machine.I2C
# On ESP32 with MicroPython
from machine import I2C

i2c = I2C(freq = 400000)
# On PC
from bridges.ftdi.controllers.i2c import I2cController
I2C = I2cController().I2C

i2c = I2C(freq = 400000)
# For machine.SPI
# On ESP32 with MicroPython
from machine import SPI

Spi = SPI(id, baudrate = 10000000, polarity = 0, phase = 0)
Spi.init()
# On PC
from bridges.ftdi.controllers.spi import SpiController
SPI = SpiController().SPI

Spi = SPI(id, baudrate = 10000000, polarity = 0, phase = 0)
Spi.init()
# For machine.Pin
# On ESP32 with MicroPython
from machine import Pin

P0 = Pin(0, Pin.OUT)
P0.value(0)
P0.value(1)

P2 = Pin(2, Pin.IN, Pin.PULL_UP)
Print(p2.value())
# On PC
from bridges.interfaces.micropython.machine import Pin
from bridges.ftdi.controllers.gpio import GpioController
machine = GpioController()

P0 = machine.Pin(0, mode = Pin.OUT)
P0.value(0)
P0.value(1)

P2 = machine.Pin(2, mode = Pin.IN)
Print(p2.value())
# For machine.UART
# On ESP32 with MicroPython
from machine import UART

Uart = UART(1, 9600)
Uart.init(9600, bits=8, parity=None, stop=1)
# On PC
from bridges.ftdi.controllers.uart import UartController
UART = UartController().UART

Uart = UART(1, 9600)
Uart.init(9600, bits=8, parity=None, stop=1)