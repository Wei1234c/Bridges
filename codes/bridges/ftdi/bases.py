# Ports
from bridges.ftdi.controllers.gpio import GpioController as GpioPort
from bridges.ftdi.controllers.i2c import I2cController
from bridges.ftdi.controllers.spi import SpiController
from bridges.ftdi.controllers.spi import SpiGpioPort
from bridges.ftdi.controllers.uart import UartController
from pyftdi.i2c import I2cPort
from pyftdi.spi import SpiPort
from pyftdi.serialext.protocol_ftdi import Serial as UartPort
