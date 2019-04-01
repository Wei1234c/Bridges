from pyftdi.serialext.protocol_ftdi import Serial as UartPort

from bridges.adapters.rpi import serial



class Serial(UartPort, serial.Serial):
    """
    Inherit from adapter framework
    """
