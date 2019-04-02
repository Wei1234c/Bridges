import pyftdi.spi

import bridges.ftdi
from bridges.ftdi.adapters.micropython import machine
from bridges.ftdi.adapters.rpi import spidev



class SpiController(bridges.ftdi.Controller, pyftdi.spi.SpiController):

    def __init__(self, silent_clock = False, cs_count = 1, turbo = True,
                 product = bridges.ftdi.DEFAULT_PRODUCT,
                 interface = bridges.ftdi.DEFAULT_INTERFACE,
                 serial_no = None,
                 **kwargs):
        pyftdi.spi.SpiController.__init__(self, silent_clock = silent_clock, cs_count = cs_count, turbo = turbo)
        bridges.ftdi.Controller.__init__(self,
                                         product = product,
                                         interface = interface,
                                         serial_no = serial_no,
                                         **kwargs)


    def get_spi(self, cs = 0, freq = None, mode = 0):
        port = self.get_port(cs, freq, mode)  # do validation.
        spi = machine.SPI(controller = self, cs = cs, spi_mode = mode)
        spi._cs_epilog = port._cs_epilog
        spi.set_frequency(port.frequency)
        self._spi_ports[cs] = spi
        return spi


    def get_spidev(self, cs = 0, freq = None, mode = 0):
        port = self.get_port(cs, freq, mode)  # do validation.
        spi = spidev.SpiDev(controller = self, cs = cs, spi_mode = mode)
        spi._cs_epilog = port._cs_epilog
        spi.set_frequency(port.frequency)
        self._spi_ports[cs] = spi
        return spi


    def SPI(self, id = -1,
            baudrate = 10000000,
            polarity = 0, phase = 0,
            bits = 8, firstbit = machine.SPI.MSB,
            sck = None, mosi = None, miso = None, pins = None,
            cs = 0):
        return self.get_spi(freq = baudrate, mode = ((polarity << 1) | phase), cs = cs)


    def SpiDev(self, bus = None, *args, **kwargs):
        return self.get_spidev()


    def get_gpio(self):
        pyftdi.spi.SpiController.get_gpio(self)  # do validation.
        self._gpio_port = SpiGpioPort(controller = self)
        return self._gpio_port


    def GPIO(self):
        return self.get_gpio()



class SpiGpioPort(pyftdi.spi.SpiGpioPort):
    VERSION = 0.1

    BOARD = 10
    BCM = 11

    IN = 1
    OUT = 0

    PUD_UP = 22
    PUD_DOWN = 21

    HIGH = 1
    LOW = 0

    RISING = 31
    FALLING = 32
    BOTH = 33


    def __init__(self, controller):
        super().__init__(controller)
        self._prepare_lookup_table()


    def __del__(self):
        self._controller = None


    def _prepare_lookup_table(self):
        # For PyFtdi, interfaces start @ one, not zero-based.
        # However, for example FT2232H has two interfaces, with USB bInterfaceNumbers start @ zero.
        self.pins_idx = bridges.ftdi.PINS_IDX[(self._controller._ftdi.ic_name,
                                               self._controller._ftdi.interface.bInterfaceNumber + 1)]
        self.pins_names = {idx: name for name, idx in self.pins_idx.items()}


    def get_pin_idx(self, pin_name):
        return self.pins_idx[pin_name]


    def get_pin_name(self, pin_idx):
        return self.pins_names[pin_idx]


    @property
    def addressable_pins(self):
        all_pins = self.all_pins
        return {name: idx for name, idx in self.pins_idx.items() if all_pins & (1 << idx)}


    def list_pins_names(self, pins_bitfield):
        return [self.get_pin_name(i) for i in range(self.width) if (1 << i) & pins_bitfield]


    def get_pin_direction(self, pin_idx):
        value = self.direction & (1 << pin_idx)
        return 1 if value else 0


    def set_pin_direction(self, pin_idx, output = False):
        pins = self._controller._gpio_mask | (1 << pin_idx)
        direction = self.direction & ~(1 << pin_idx) | (int(output) << pin_idx)
        self.set_direction(pins, direction)


    @property
    def pins_values(self):
        return self.read(with_output = True)


    @property
    def pins_values_list(self):
        values = self.pins_values
        return [1 if values & (1 << idx) else 0
                for idx in sorted(self.pins_idx.values())]


    def get_pin_value(self, pin_idx):
        value = self.pins_values & (1 << pin_idx)
        return 1 if value else 0


    def set_pin_value(self, pin_idx, level):
        level = 1 if level else 0
        status = self.read(with_output = True) & self.direction
        clear_mask = (1 << self.width) - 1 - (1 << pin_idx)
        value = status & clear_mask | (level << pin_idx)
        self.write(value)


    def setup(self, channel, mode, pull_up_down = None, initial = None):
        if hasattr(channel, '__len__'):
            for ch in channel:
                self.setup(ch, mode, initial)
        else:
            mode = 3 if mode == 0 else mode
            return self.Pin(channel, mode, pull = pull_up_down, value = initial)


    def Pin(self, id,
            mode = machine.Pin.IN, pull = None,
            value = None,
            drive = None, alt = None):

        assert id in self.addressable_pins.keys() or \
               id in self.addressable_pins.values(), \
            'Invalid pin: {}.\n Addressable pins: {}'.format(id, self.addressable_pins)
        return machine.Pin(id, mode, pull, value, drive, alt, gpio_port = self)


    def PinDummy(self):

        return machine.PinDummy()
