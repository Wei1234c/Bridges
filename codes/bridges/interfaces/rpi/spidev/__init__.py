# https://github.com/doceme/py-spidev/blob/master/spidev_module.c
# https://github.com/doceme/py-spidev


class SpiDev:
    """
    SpiDev([bus],[client]) -> SPI

    Return a new SPI object that is (optionally) connected to the
    specified SPI device interface.
    """


    def __init__(self, bus = None, *args, **kwargs):
        raise NotImplementedError()


    def __enter__(self, *args, **kwargs):
        raise NotImplementedError()


    def __exit__(self, *args, **kwargs):
        raise NotImplementedError()


    def close(self):
        """
        close()

        Disconnects the object from the interface.
        """
        raise NotImplementedError()


    def fileno(self):
        """
        fileno() -> integer "file descriptor"

        This is needed for lower-level file interfaces, such as os.read().
        """
        raise NotImplementedError()


    def open(self, bus, device):
        """
        open(bus, device)

        Connects the object to the specified SPI device.
        open(X,Y) will open /dev/spidev<X>.<Y>
        """
        raise NotImplementedError()


    def readbytes(self, *args, **kwargs):
        """
        read(len) -> [values]

        Read len bytes from SPI device.
        """
        raise NotImplementedError()


    def writebytes(self, *args, **kwargs):
        """
        write([values]) -> None

        Write bytes to SPI device.
        """
        raise NotImplementedError()


    def writebytes2(self, values = None):
        """
        writebytes2([values]) -> None

        Write bytes to SPI device.
        values must be a list or buffer.
        """
        raise NotImplementedError()


    def xfer(self, values = None):
        """
        xfer([values]) -> [values]

        Perform SPI transaction.
        CS will be released and reactivated between blocks.
        delay specifies delay in usec between blocks.
        """
        raise NotImplementedError()


    def xfer2(self, values = None):
        """
        xfer2([values]) -> [values]

        Perform SPI transaction.
        CS will be held active between blocks.
        """
        raise NotImplementedError()


    def xfer3(self, values = None):
        """
        xfer3([values]) -> [values]

        Perform SPI transaction. Accepts input of arbitrary size.
        Large blocks will be send as multiple transactions
        CS will be held active between blocks.
        """
        raise NotImplementedError()


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
        """LSB first"""
        raise NotImplementedError()


    @lsbfirst.setter
    def lsbfirst(self, bits):
        raise NotImplementedError()


    @property
    def max_speed_hz(self):
        """maximum speed in Hz"""
        raise NotImplementedError()


    @max_speed_hz.setter
    def max_speed_hz(self, bits):
        raise NotImplementedError()


    @property
    def mode(self):
        """SPI mode as two bit pattern of
        Clock Polarity  and Phase [CPOL|CPHA]
        min: 0b00 = 0 max: 0b11 = 3
        """
        raise NotImplementedError()


    @mode.setter
    def mode(self, bits):
        raise NotImplementedError()


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
