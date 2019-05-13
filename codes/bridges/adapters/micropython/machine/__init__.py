from array import array

from bridges.interfaces import *



class Pin(I_machine.Pin):

    def __init__(self, id, mode = I_machine.Pin.IN, pull = None, value = None,
                 drive = None, alt = None,
                 invert = False,
                 gpio_port = None):

        self._gpio_port = gpio_port

        if not isinstance(id, int):
            try:
                id = self._gpio_port.get_pin_idx(id)
            except KeyError:
                raise KeyError('No such pin as {}.'.format(id))

        self._id = id
        self._mode = mode
        self._bit_mask = 1 << id
        self._pull = pull
        self._drive = drive
        self._alt = alt
        self._invert = invert

        self.init(mode, value)


    def __del__(self):
        self._gpio_port = None


    def init(self, mode = None, value = None, invert = False):
        self._invert = invert
        self.mode(mode)
        if self.mode() == self.OUT:
            self.value(I_machine.Pin.LOW if value is None else value)
        return self


    @property
    def pin_id(self):
        return self._id


    def value(self, value = None):
        if value is None:
            return self._gpio_port.get_pin_value(self._id)
        else:
            self._gpio_port.set_pin_value(self._id, value)


    def high(self):
        self.value(I_machine.Pin.HIGH)


    def low(self):
        self.value(I_machine.Pin.LOW)


    def on(self):
        self.low() if self._invert else self.high()


    def off(self):
        self.high() if self._invert else self.low()


    def toggle(self):
        self.value(not self.value())


    def irq(self, handler = None,
            trigger = (I_machine.Pin.IRQ_FALLING | I_machine.Pin.IRQ_RISING),
            priority = 1, wake = None, hard = False):
        raise NotImplementedError('Not supported.')


    def mode(self, mode = None):
        if mode is None:
            return self._mode
        else:
            assert mode in (I_machine.Pin.IN, I_machine.Pin.OUT), 'Only Pin.IN, Pin.OUT supported.'
            self._mode = mode
            self._gpio_port.set_pin_direction(self._id, 1 if self._mode == self.OUT else 0)


    def pull(self, pull = None):
        if pull is None:
            return self._pull
        else:
            self._pull = pull


    def drive(self, drive = None):
        if drive is None:
            return self._drive
        else:
            self._drive = drive



class Signal(Pin):
    """
    Inherit from Pin
    """



class PinDummy(Pin):

    def __init__(self):
        pass


    def __del__(self):
        pass


    def value(self, value = None):
        pass


    def mode(self, mode = None):
        pass



class I2C(I_machine.I2C):

    def __init__(self, id = -1, scl = None, sda = None, freq = 400000):
        self.init(scl, sda, freq)


    def __del__(self):
        self._controller = None


    def init(self, scl, sda, freq = 400000):
        self.set_speed(freq)


    def deinit(self):
        print('Not Applicable.')


    def set_speed(self, frequency = 400000):
        self._controller._set_frequency(frequency * 2 / 3)


    def scan(self):
        addrs = []
        slaves = []
        for addr in range(I_smbus2.HIGHEST_I2C_ADDRESS + 1):
            self._address = addr

            if self.poll(write = True):
                slaves.append('X')
                addrs.append(addr)
            else:
                slaves.append('.')

        columns = 16
        row = 0
        print('   %s' % ''.join(' %01X ' % col for col in range(columns)))

        while True:
            chunk = slaves[row:row + columns]
            if not chunk:
                break
            print(' %1X:' % (row // columns), '  '.join(chunk))
            row += columns

        print("\nFound devices at:", [hex(addr) for addr in addrs])
        return addrs


    def start(self):
        self._controller._do_start()


    def stop(self):
        self._controller._do_stop()


    def readinto(self, buf, nack = True):
        buf[:] = self.read(len(buf), relax = nack, start = False)


    def write(self, buf):
        raise NotImplementedError()


    def readfrom(self, addr, nbytes, stop = True):
        self._address = addr
        return self.read(nbytes, relax = stop)


    def readfrom_into(self, addr, buf, stop = True):
        buf[:] = self.readfrom(addr, len(buf), stop)


    def writeto(self, addr, buf, stop = True):
        raise NotImplementedError()


    def readfrom_mem(self, addr, memaddr, nbytes, addrsize = 8):
        self._address = addr
        return self.read_from(memaddr, nbytes)


    def readfrom_mem_into(self, addr, memaddr, buf, addrsize = 8):
        value = self.readfrom_mem(addr, memaddr, len(buf), addrsize)
        buf[:] = value


    def writeto_mem(self, addr, memaddr, buf, addrsize = 8):
        self._address = addr
        return self.write_to(memaddr, buf)



class SPI(I_machine.SPI):
    LSB = 1
    MSB = 0


    def __init__(self, id = -1, baudrate = 10000000, polarity = 0, phase = 0, bits = 8, firstbit = MSB,
                 sck = None, mosi = None, miso = None, pins = None):
        raise NotImplementedError()


    def __del__(self):
        self.close()


    def init(self, baudrate = 10000000, polarity = 0, phase = 0, bits = 8, firstbit = MSB,
             sck = None, mosi = None, miso = None, pins = None):
        pass


    def close(self):
        self._controller = None


    def deinit(self):
        self.close()


    def read(self, nbytes, write = 0x00):
        raise NotImplementedError()


    def readinto(self, buf, write = 0x00):
        buf[:] = self.read(len(buf))


    def write(self, buf):
        raise NotImplementedError()


    def write_readinto(self, write_buf, read_buf, start = True, stop = True):
        write_buf = array('B', write_buf)
        read_buf[:] = self.exchange(out = write_buf, readlen = len(write_buf),
                                    start = start, stop = stop, duplex = True)


    def transfer(self, pin_ss, address, value = 0x00):
        response = bytearray(1)

        pin_ss.low()

        self.write(bytes([address]), stop = False)
        self.write_readinto(bytes([value]), response, start = False)

        pin_ss.high()

        return response



class UART(I_machine.UART):

    def __init__(self, id = -1, baudrate = 9600, bits = 8, parity = None, stop = 1,
                 *args, **kwargs):
        raise NotImplementedError()


    def init(self, baudrate = 9600, bits = 8, parity = None, stop = 1,
             tx = None, rx = None, txbuf = None, rxbuf = None,
             xonxoff = False, rtscts = False):
        self._baudrate = baudrate
        self._bytesize = bits
        self._stopbits = stop
        self._parity = parity
        self._rtscts = rtscts
        self._xonxoff = xonxoff

        self._reconfigure_port()


    def deinit(self):
        pass


    def any(self):
        return len(self.udev.readbuffer)


    def read(self, nbytes):
        raise NotImplementedError()


    def readinto(self, buf, nbytes = None):
        buf[:] = self.read(nbytes)


    def readline(self):
        return self.read_until()


    def write(self, buf):
        raise NotImplementedError()


    def sendbreak(self):
        self.send_break()


    def irq(self, trigger, priority = 1, handler = None, wake = I_machine.IDLE):
        raise NotImplementedError()
