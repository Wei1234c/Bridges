from bridges.adapters.rpi import gpio
from bridges.ch341A.controllers.gpio import GpioPort



class GPIO(GpioPort, gpio.GPIO):
    """
    Inherit from adapter framework
    """