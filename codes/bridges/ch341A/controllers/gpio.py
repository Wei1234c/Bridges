from bridges.ftdi.controllers.spi import SpiGpioPort


PINS_IDX = {'D0': 0, 'D1': 1, 'D2': 2, 'D3': 3, 'D4': 4, 'D5': 5, 'D6': 6, 'D7': 7}



class GpioPort(SpiGpioPort):
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


    def __init__(self, device, direction = 0, value = 0, **kwargs):

        self._device = device
        self._direction = direction
        self._value = value
        self._prepare_lookup_table()


    def __del__(self):
        self.terminate()


    def terminate(self):
        self._device = None


    def _prepare_lookup_table(self):
        self.pins_idx = PINS_IDX
        self.pins_names = {idx: name for name, idx in self.pins_idx.items()}


    @property
    def width(self):
        return len(self.pins_idx)


    @property
    def all_pins(self):
        return (1 << self.width) - 1


    @property
    def gpio_mask(self):
        return self.all_pins


    @property
    def direction(self):
        return self._direction


    def set_pin_direction(self, pin_idx, output = False):
        pins = self.gpio_mask | (1 << pin_idx)
        direction = self.direction & ~(1 << pin_idx) | (int(output) << pin_idx)
        self.set_direction(pins, direction)


    def set_direction(self, pins, direction):
        if (pins & self.gpio_mask) != pins:
            raise ValueError('No such GPIO pin(s)')
        self._direction &= ~pins
        self._direction |= (pins & direction)
        # self._gpio_mask = gpio_mask & pins


    def read(self, with_output = True):
        # todo: replace this with real "read" function.
        return self._value


    def _list_bitsmap(self, bits):
        return [self.get_pin_name(i) for i in range(self.width) if (1 << i) & bits]


    def write(self, value):
        self._value = value
        self._device.set_output2(output_pins = self._list_bitsmap(self.direction),
                                 high_pins = self._list_bitsmap(value))
