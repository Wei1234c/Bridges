from pyftdi.usbtools import UsbToolsError

from bridges import config


DEFAULT_PRODUCT = config.FTDI_DEFAULT_PRODUCT
DEFAULT_INTERFACE = config.FTDI_DEFAULT_INTERFACE

PINS_IDX = {('ft232h', 1) : {'ADBUS0': 0, 'ADBUS1': 1, 'ADBUS2': 2, 'ADBUS3': 3, 'ADBUS4': 4, 'ADBUS5': 5, 'ADBUS6': 6,
                             'ADBUS7': 7,
                             'ACBUS0': 8, 'ACBUS1': 9, 'ACBUS2': 10, 'ACBUS3': 11, 'ACBUS4': 12, 'ACBUS5': 13,
                             'ACBUS6': 14,
                             'ACBUS7': 15},
            ('ft2232h', 1): {'ADBUS0': 0, 'ADBUS1': 1, 'ADBUS2': 2, 'ADBUS3': 3, 'ADBUS4': 4, 'ADBUS5': 5, 'ADBUS6': 6,
                             'ADBUS7': 7,
                             'ACBUS0': 8, 'ACBUS1': 9, 'ACBUS2': 10, 'ACBUS3': 11, 'ACBUS4': 12, 'ACBUS5': 13,
                             'ACBUS6': 14,
                             'ACBUS7': 15},
            ('ft2232h', 2): {'BDBUS0': 0, 'BDBUS1': 1, 'BDBUS2': 2, 'BDBUS3': 3, 'BDBUS4': 4, 'BDBUS5': 5, 'BDBUS6': 6,
                             'BDBUS7': 7,
                             'BCBUS0': 8, 'BCBUS1': 9, 'BCBUS2': 10, 'BCBUS3': 11, 'BCBUS4': 12, 'BCBUS5': 13,
                             'BCBUS6': 14,
                             'BCBUS7': 15}}



class URL:

    def __init__(self, protocol = 'ftdi',
                 vendor = 'ftdi', product = DEFAULT_PRODUCT, index = None, serial_no = None,
                 interface = DEFAULT_INTERFACE):
        self.protocol = protocol
        self.vendor = vendor
        self.product = product
        self.index = index
        self.serial_no = serial_no
        self.interface = interface


    def string(self, interface = None):
        interface = self.interface if interface is None else interface
        return '{}://{}:{}{}{}/{}'.format(self.protocol, self.vendor, self.product,
                                          ':' if self.index is None else ':{}'.format(self.index),
                                          ':' if self.serial_no is None else ':{}'.format(self.serial_no), interface)



class Controller:

    def __init__(self, protocol = 'ftdi',
                 vendor = 'ftdi', product = None, index = None, serial_no = None,
                 interface = 1, **kwargs):
        self.url = URL(protocol, vendor, product, index, serial_no, interface)
        self.configure(self.url.string(), **kwargs)


    def __enter__(self):
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__del__()


    def __del__(self):
        if self.is_open:
            self.terminate()


    def close(self):
        self.terminate()


    @property
    def is_open(self):
        try:
            return self._ftdi.usb_dev is not None
        except (UsbToolsError, AttributeError) as e:
            print(e)
