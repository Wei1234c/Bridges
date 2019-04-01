from pyftdi.serialext.protocol_ftdi import Serial as UartPort

from bridges.adapters.rpi import serial



class Serial(UartPort, serial.Serial):

    def __init__(self, url, *args, **kwargs):
        UartPort.__init__(self, url, *args, **kwargs)
        serial.Serial.__init__(self, *args, **kwargs)
        self.port = url
