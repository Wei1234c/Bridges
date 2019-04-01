from pyftdi.serialext.protocol_ftdi import Serial as UartPort
from pyftdi.spi import SpiPort

from bridges.adapters.micropython import machine
from bridges.ch341A.controllers.i2c import I2cPort



class Pin(machine.Pin):
    """
    Inherit from adapter framework
    """



class PinDumy(machine.Pin):
    """
    Inherit from adapter framework
    """



class I2C(I2cPort, machine.I2C):

    def __init__(self, id = -1, scl = None, sda = None, freq = 400000,
                 controller = None, address = None):
        I2cPort.__init__(self, controller, address)
        machine.I2C.__init__(self, id, scl, sda, freq)


    def write(self, buf):
        I2cPort.write(self, buf, relax = True, start = False)


    def writeto(self, addr, buf, stop = True):
        self._address = addr
        I2cPort.write(self, buf, relax = stop, start = True)



class SPI(SpiPort, machine.SPI):
    LSB = 1
    MSB = 0


    def __init__(self, id = -1, baudrate = 10000000, polarity = 0, phase = 0, bits = 8, firstbit = MSB,
                 sck = None, mosi = None, miso = None, pins = None,
                 controller = None, cs = 0, cs_hold = 3, spi_mode = 0):
        mode = ((polarity << 1) | phase) if spi_mode is None else spi_mode
        SpiPort.__init__(self, controller, cs, cs_hold, mode)


    def read(self, nbytes, write = 0x00):
        return SpiPort.read(self, nbytes)


    def write(self, buf):
        SpiPort.write(self, buf)



class UART(UartPort, machine.UART):

    def read(self, nbytes):
        return UartPort.read(self, nbytes)


    def write(self, buf):
        return UartPort.write(self, buf)
