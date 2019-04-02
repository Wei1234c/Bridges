IDLE = 4



# https://docs.micropython.org/en/latest/library/machine.Pin.html
class Pin:
    IN = 1
    OUT = 3

    LOW = 0
    HIGH = 1

    IRQ_RISING = 1
    IRQ_FALLING = 2
    IRQ_LOW_LEVEL = None
    IRQ_HIGH_LEVEL = None

    PULL_UP = 0
    PULL_DOWN = 1
    PULL_HOLD = None
    OPEN_DRAIN = 7

    WAKE_LOW = 4
    WAKE_HIGH = 5

    ALT = None
    ALT_OPEN_DRAIN = None

    LOW_POWER = None
    MED_POWER = None
    HIGH_POWER = None


    def __init__(self, id, mode = -1, pull = -1, value = None, drive = None, alt = None):
        raise NotImplementedError()


    def init(self):
        raise NotImplementedError()


    @property
    def pin_id(self):
        raise NotImplementedError()


    def irq(self):
        raise NotImplementedError()


    def value(self, value = None):
        raise NotImplementedError()


    def high(self):
        raise NotImplementedError()


    def low(self):
        raise NotImplementedError()


    def __call__(self, value = None):
        return self.value(value)


    def on(self):
        self.value(1)


    def off(self):
        self.value(0)


    def irq(self, handler = None, trigger = (IRQ_FALLING | IRQ_RISING),
            priority = 1, wake = None, hard = False):
        raise NotImplementedError()


    def mode(self, mode = None):
        raise NotImplementedError()


    def pull(self, pull = None):
        raise NotImplementedError()


    def drive(self, drive = None):
        raise NotImplementedError()



# https://docs.micropython.org/en/latest/library/machine.I2C.html#
class I2C:

    def __init__(self, id, scl, sda, freq = 400000):
        raise NotImplementedError()


    def init(self, scl, sda, freq = 400000):
        raise NotImplementedError()


    def deinit(self):
        raise NotImplementedError()


    def scan(self):
        raise NotImplementedError()


    def start(self):
        raise NotImplementedError()


    def stop(self):
        raise NotImplementedError()


    def readinto(self, buf, nack = True):
        raise NotImplementedError()


    def write(self, buf):
        raise NotImplementedError()


    def readfrom(self, addr, nbytes, stop = True):
        raise NotImplementedError()


    def readfrom_into(self, addr, buf, stop = True):
        raise NotImplementedError()


    def writeto(self, addr, buf, stop = True):
        raise NotImplementedError()


    def readfrom_mem(self, addr, memaddr, nbytes, addrsize = 8):
        raise NotImplementedError()


    def readfrom_mem_into(self, addr, memaddr, buf, addrsize = 8):
        raise NotImplementedError()


    def writeto_mem(self, addr, memaddr, buf, addrsize = 8):
        raise NotImplementedError()



# https://docs.micropython.org/en/latest/library/machine.SPI.html
class SPI:
    LSB = 1
    MSB = 0


    def __init__(self, id = -1, baudrate = 10000000, polarity = 0, phase = 0, bits = 8, firstbit = MSB,
                 sck = None, mosi = None, miso = None):
        raise NotImplementedError()


    def init(self):
        raise NotImplementedError()


    def close(self):
        raise NotImplementedError()


    def deinit(self):
        raise NotImplementedError()


    def read(self, nbytes, write = 0x00):
        raise NotImplementedError()


    def readinto(self, buf, write = 0x00):
        raise NotImplementedError()


    def write(self, buf):
        raise NotImplementedError()


    def write_readinto(self, write_buf, read_buf):
        raise NotImplementedError()


    def transfer(self, pin_ss, address, value = 0x00):
        raise NotImplementedError()



# https://docs.micropython.org/en/latest/library/machine.UART.html
class UART:

    def __init__(self, id = -1, baudrate = 9600):
        raise NotImplementedError()


    def init(self, baudrate = 9600, bits = 8, parity = None, stop = 1,
             tx = None, rx = None, txbuf = None, rxbuf = None):
        raise NotImplementedError()


    def deinit(self):
        raise NotImplementedError()


    def any(self):
        raise NotImplementedError()


    def read(nbytes):
        raise NotImplementedError()


    def readinto(buf, nbytes = None):
        raise NotImplementedError()


    def readline(self):
        raise NotImplementedError()


    def write(self, buf):
        raise NotImplementedError()


    def sendbreak(self):
        raise NotImplementedError()


    def irq(self, trigger, priority = 1, handler = None, wake = IDLE):
        raise NotImplementedError()
