from array import array

from bridges.interfaces import *



class SpiDev( I_spidev.SpiDev):

    def __init__(self, bus = None,
                 controller = None, cs = 0, cs_hold = 3, spi_mode = 0,
                 *args, **kwargs):
        raise NotImplementedError()


    def __enter__(self, *args, **kwargs):
        return self


    def __exit__(self, *args, **kwargs):
        self._controller = None


    def __del__(self):
        self._controller = None


    def open(self, bus, device):
        pass


    def close(self):
        pass


    def fileno(self):
        raise NotImplementedError()


    def readbytes(self, nbytes, *args, **kwargs):
        return self.read(nbytes)


    def writebytes(self, values = None, *args, **kwargs):
        # values = array.array('B', values)
        self.write(values)


    def writebytes2(self, values = None):
        self.writebytes(values)


    def xfer(self, values = None):
        values = array('B', values)
        return self.exchange(out = values, readlen = len(values), duplex = True)


    def xfer2(self, values = None):
        return self.xfer(values)


    def xfer3(self, values = None):
        return self.xfer(values)


    def transfer(self, pin_ss, address, value = 0x00):
        response = bytearray(1)

        pin_ss.low()
        response.append(self.xfer2([address, value])[1])
        pin_ss.high()

        return response


    @property
    def bits_per_word(self):
        """bits per word"""
        raise NotImplementedError()


    @bits_per_word.setter
    def bits_per_word(self, bits):
        raise NotImplementedError()


    @property
    def cshigh(self):
        """CS active high"""
        raise NotImplementedError()


    @cshigh.setter
    def cshigh(self, bits):
        raise NotImplementedError()


    @property
    def loop(self):
        """loopback configuration"""
        raise NotImplementedError()


    @loop.setter
    def loop(self, bits):
        raise NotImplementedError()


    @property
    def lsbfirst(self):
        return self._lsbfirst


    @lsbfirst.setter
    def lsbfirst(self, bits):
        self._lsbfirst = bits


    @property
    def max_speed_hz(self):
        return self.frequency


    @max_speed_hz.setter
    def max_speed_hz(self, frequency):
        self.set_frequency(frequency)


    @property
    def mode(self):
        return (self._cpol << 1) | self._cpha


    @mode.setter
    def mode(self, spi_mode):
        self._cpol = spi_mode & 0x1
        self._cpha = spi_mode & 0x2


    @property
    def no_cs(self):
        """disable chip select"""
        raise NotImplementedError()


    @no_cs.setter
    def no_cs(self, bits):
        raise NotImplementedError()


    @property
    def threewire(self):
        """SI/SO signals shared"""
        raise NotImplementedError()


    @threewire.setter
    def threewire(self, bits):
        raise NotImplementedError()
