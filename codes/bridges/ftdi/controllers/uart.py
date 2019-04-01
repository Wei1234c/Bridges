import bridges.ftdi

from bridges.ftdi.adapters.micropython import machine
from bridges.ftdi.adapters.rpi import serial



class UartController(bridges.ftdi.Controller):

    def __init__(self,
                 product = bridges.ftdi.DEFAULT_PRODUCT,
                 interface = bridges.ftdi.DEFAULT_INTERFACE,
                 serial_no = None,
                 **kwargs):
        bridges.ftdi.Controller.__init__(self, product = product, interface = interface, serial_no = serial_no, **kwargs)
        self.ports = {}


    @property
    def is_open(self):
        return len(self.ports.keys()) > 0


    def configure(self, url, **kwargs):
        pass


    def terminate(self):
        for port in self.ports.values():
            port.close()
        del self.ports


    def get_serial(self, interface = None, *args, **kwargs):
        def _get_serial():

            do_open = not kwargs.pop('do_not_open', False)
            uart = serial.Serial(url = self.url.string(interface), *args, **kwargs)
            if do_open:
                uart.open()
            return uart


        return self.ports.setdefault(interface, _get_serial())


    def Serial(self, interface = None, *args, **kwargs):
        return self.get_serial(interface = interface, *args, **kwargs)


    def get_uart(self, id = -1, baudrate = 9600, bits = 8, parity = None, stop = 1,
                 interface = None, *args, **kwargs):
        def _get_uart():

            do_open = not kwargs.pop('do_not_open', False)
            uart = machine.UART(id = id, baudrate = baudrate, bits = bits, parity = parity, stop = stop,
                                url = self.url.string(interface), *args, **kwargs)
            if do_open:
                uart.open()
            return uart


        return self.ports.setdefault(interface, _get_uart())


    def UART(self, id = -1, baudrate = 9600, bits = 8, parity = None, stop = 1,
             interface = None, *args, **kwargs):
        return self.get_uart(id = id, baudrate = baudrate, bits = bits,
                             parity = 'N' if parity is None else parity, stop = stop,
                             interface = interface, *args, **kwargs)
