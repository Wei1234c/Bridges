from bridges.adapters.rpi import smbus2

from bridges.ch341A.controllers.i2c import I2cPort



class SMBus(I2cPort, smbus2.SMBus):

    def __init__(self, bus = None, force = False, controller = None, address = None):
        I2cPort.__init__(self, controller, address)
