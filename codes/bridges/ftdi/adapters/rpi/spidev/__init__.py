from pyftdi.spi import SpiPort

from bridges.adapters.rpi import spidev



class SpiDev(SpiPort, spidev.SpiDev):

    def __init__(self, bus = None,
                 controller = None, cs = 0, cs_hold = 3, spi_mode = 0,
                 *args, **kwargs):
        SpiPort.__init__(self, controller, cs, cs_hold, spi_mode)
        self.lsbfirst = False
