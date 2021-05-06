import pyftdi.gpio

import bridges.ftdi.controllers.spi



class GpioController(bridges.ftdi.Controller,
                     pyftdi.gpio.GpioController,
                     bridges.ftdi.controllers.spi.SpiGpioPort):

    def __init__(self, silent_clock = False, cs_count = 1, turbo = True,
                 product = bridges.ftdi.DEFAULT_PRODUCT,
                 interface = bridges.ftdi.DEFAULT_INTERFACE,
                 serial_no = None,
                 direction = 0, **kwargs):

        pyftdi.gpio.GpioController.__init__(self)

        kwargs['direction'] = direction
        bridges.ftdi.Controller.__init__(self,
                                         product = product,
                                         interface = interface,
                                         serial_no = serial_no,
                                         **kwargs)
        self._controller = self
        self._prepare_lookup_table()


    def terminate(self):
        if self._ftdi:
            self._ftdi.close()


    def get_gpio(self):
        return self


    @property
    def all_pins(self):
        return self._mask


    def set_pin_direction(self, pin_idx, output = False):
        pins = self._mask | (1 << pin_idx)
        direction = self.direction & ~(1 << pin_idx) | (int(output) << pin_idx)
        self.set_direction(pins, direction)


    @property
    def width(self):
        return self._mask.bit_length()


    @property
    def pins_values(self):
        return pyftdi.gpio.GpioController.read(self)


    def set_pin_value(self, pin_idx, level):
        level = 1 if level else 0
        clear_mask = (1 << self.width) - 1 - (1 << pin_idx)
        value = self.pins_values & clear_mask | (level << pin_idx)
        self.write(value)
