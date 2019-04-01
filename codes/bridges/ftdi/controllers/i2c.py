from array import array

import pyftdi.i2c

import bridges.ftdi
from bridges.ftdi.adapters.micropython import machine
from bridges.ftdi.adapters.rpi import smbus2



class I2cController(bridges.ftdi.Controller, pyftdi.i2c.I2cController):

    def __init__(self,
                 product = bridges.ftdi.DEFAULT_PRODUCT,
                 interface = bridges.ftdi.DEFAULT_INTERFACE,
                 serial_no = None,
                 **kwargs):
        pyftdi.i2c.I2cController.__init__(self)
        bridges.ftdi.Controller.__init__(self,
                                         product = product,
                                         interface = interface,
                                         serial_no = serial_no,
                                         **kwargs)


    def _set_frequency(self, frequency):
        self._ftdi.set_frequency(frequency)


    def get_i2c(self, address = None, freq = 400000):
        port = machine.I2C(controller = self, address = address, freq = freq)
        return self._get_port(port, address)


    def I2C(self, id = -1, scl = None, sda = None, freq = 400000):
        return self.get_i2c(freq = freq)


    def get_smbus(self, address = None):

        port = smbus2.SMBus(bus = None, force = False, controller = self, address = address)
        return self._get_port(port, address)


    def SMBus(self, bus = None, force = False):
        return self.get_smbus()


    def _get_port(self, port, address):
        if not self._ftdi:
            raise pyftdi.i2c.I2cIOError("FTDI controller not initialized")

        if address is not None:
            self.validate_address(address)
            if address not in self._slaves:
                self._slaves[address] = port
        else:
            self._slaves[port.__hash__()] = port
        return port


    def _do_start(self):
        cmd = array('B', self._idle)
        cmd.extend(self._start)
        self._ftdi.write_data(cmd)


    def _do_stop(self):
        cmd = array('B', self._stop)
        self._ftdi.write_data(cmd)
