import array



class Pin:

    def low(self):
        raise NotImplementedError()


    def high(self):
        raise NotImplementedError()


    def value(self):
        raise NotImplementedError()


    def set_handler_for_irq_on_rising_edge(self, handler):
        raise NotImplementedError()


    def detach_irq(self):
        raise NotImplementedError()


    @classmethod
    def from_uPy(cls, pin):
        if pin:
            return Pin_uPy(pin)


    @classmethod
    def from_RPi(cls, GPIO, pin_id, is_output = True):
        if GPIO and pin_id:
            return Pin_RPi(GPIO, pin_id, is_output)



class Pin_uPy(Pin):

    def __init__(self, pin):
        self.pin = pin


    def low(self):
        return self.pin.value(0)


    def high(self):
        return self.pin.value(1)


    def value(self):
        return self.pin.value()


    def set_handler_for_irq_on_rising_edge(self, handler):
        return self.pin.irq(handler = handler, trigger = self.pin.IRQ_RISING)


    def detach_irq(self):
        return self.pin.irq(handler = None, trigger = 0)



class Pin_RPi(Pin):

    def __init__(self, GPIO, pin_id, is_output = True):
        self.GPIO = GPIO
        self.pin_id = pin_id
        GPIO.setup(pin_id, GPIO.OUT if is_output else GPIO.IN)


    def low(self):
        return self.GPIO.output(self.pin_id, self.GPIO.LOW)


    def high(self):
        return self.GPIO.output(self.pin_id, self.GPIO.HIGH)


    def value(self):
        return self.GPIO.input(self.pin_id)


    def set_handler_for_irq_on_rising_edge(self, handler):
        return self.GPIO.add_event_detect(self.pin_id, self.GPIO.RISING, callback = handler)


    def detach_irq(self):
        return self.GPIO.remove_event_detect(self.pin_id)



class SPI:

    def transfer(self, address, value = 0x00):
        raise NotImplementedError()


    @classmethod
    def from_uPy(cls, spi, pin_ss = None):
        return SPI_uPy(spi, pin_ss)


    @classmethod
    def from_RPi(cls, spi, GPIO = None, pin_ss_id = None):
        return SPI_RPi(spi, GPIO, pin_ss_id)



class SPI_uPy(SPI):

    def __init__(self, spi, pin_ss = None):
        self.spi = spi
        self.pin_ss = Pin.from_uPy(pin_ss)
        self.close = spi.deinit


    def transfer(self, address, value = 0x00):
        response = bytearray(1)
        if self.pin_ss:
            self.pin_ss.low()
        self.spi.write(bytes([address]))
        self.spi.write_readinto(bytes([value]), response)
        if self.pin_ss:
            self.pin_ss.high()

        return response



class SPI_RPi(SPI):

    def __init__(self, spi, GPIO = None, pin_ss_id = None):
        self.spi = spi
        self.pin_ss = Pin.from_RPi(GPIO, pin_ss_id, is_output = True)
        self.close = spi.close


    def transfer(self, address, value = 0x00):
        response = bytearray(1)
        if self.pin_ss:
            self.pin_ss.low()
        response.append(self.spi.xfer2([address, value])[1])
        if self.pin_ss:
            self.pin_ss.high()

        return response



class I2C:

    def __init__(self, i2c):
        self.i2c = i2c


    def readfrom(self, addr, nbytes, stop = True):
        raise NotImplementedError()


    def writeto(self, addr, buf, stop = True):
        raise NotImplementedError()


    @classmethod
    def from_uPy(cls, i2c):
        return I2C_uPy(i2c)


    @classmethod
    def from_RPi(cls, i2c):
        return I2C_RPi(i2c)



class I2C_uPy(I2C):

    def readfrom(self, addr, nbytes, stop = True):
        return self.i2c.readfrom(addr, nbytes, stop)


    def writeto(self, addr, buf, stop = True):
        return self.i2c.writeto(addr, buf, stop)



class I2C_RPi(I2C):

    def readfrom(self, addr, nbytes, stop = True):
        return array.array('B', [self.i2c.read_byte(addr) for i in range(len(nbytes))])


    def writeto(self, addr, buf, stop = True):
        return sum([self.i2c.write_byte(addr, buf[i]) for i in range(len(buf))])
