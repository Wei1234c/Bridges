import bridges
from bridges.adapters.rpi import gpio
from bridges.ftdi.controllers.gpio import GpioController as GpioPort



class Gpio(GpioPort, gpio.GPIO):

    def __init__(self, silent_clock = False, cs_count = 1, turbo = True,
                 product = bridges.ftdi.DEFAULT_PRODUCT,
                 interface = bridges.ftdi.DEFAULT_INTERFACE,
                 serial_no = None,
                 direction = 0, *args, **kwargs):
        GpioPort.__init__(self, silent_clock = silent_clock, cs_count = cs_count, turbo = turbo,
                          product = product,
                          interface = interface,
                          serial_no = serial_no,
                          direction = direction, *args, **kwargs)
