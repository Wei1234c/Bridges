from array import array

from bridges.interfaces import *



class SMBus(I_smbus2.SMBus):

    def __init__(self, bus = None, force = False):
        raise NotImplementedError()


    def __enter__(self):
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        self._controller = None


    def __del__(self):
        self._controller = None


    def open(self, bus):
        print('Not Applicable.')


    def close(self):
        print('Not Applicable.')


    def _set_address(self, address, force = None):
        self._address = address


    def _get_funcs(self):
        raise NotImplementedError()


    def write_quick(self, i2c_addr, force = None):
        self._set_address(i2c_addr)
        self.write(array('B', []))


    def read_byte(self, i2c_addr, force = None):
        self._set_address(i2c_addr)
        return self.read(1)[0]


    def write_byte(self, i2c_addr, value, force = None):
        self._set_address(i2c_addr)
        self.write(array('B', [value]))


    def read_byte_data(self, i2c_addr, register, force = None):
        self._set_address(i2c_addr)
        return self.read_from(register, 1)[0]


    def write_byte_data(self, i2c_addr, register, value, force = None):
        self._set_address(i2c_addr)
        self.write_to(register, array('B', [value]))


    def read_word_data(self, i2c_addr, register, force = None):
        self._set_address(i2c_addr)
        value = self.read_from(register, 2)
        return (value[0] << 8) + value[1]


    def write_word_data(self, i2c_addr, register, value, force = None):
        self._set_address(i2c_addr)
        data = array('B', [(value >> 8) & 0xff, value & 0xff])
        self.write_to(register, data)


    def process_call(self, i2c_addr, register, value, force = None):
        self._set_address(i2c_addr)
        self.write_to(register, array('B', value), relax = False)
        return self.read_from(register, len(value), start = False)


    def read_block_data(self, i2c_addr, register, force = None):
        self._set_address(i2c_addr)
        return self.read_from(register, I_smbus2.I2C_SMBUS_BLOCK_MAX)


    def write_block_data(self, i2c_addr, register, data, force = None):
        self._set_address(i2c_addr)
        return self.write_to(register, data)


    def block_process_call(self, i2c_addr, register, data, force = None):
        self._set_address(i2c_addr)
        self.write_to(register, data, relax = False)
        return self.read_from(register, len(data), start = False)


    def read_i2c_block_data(self, i2c_addr, register, length, force = None):
        self._set_address(i2c_addr)
        return self.read_from(register, length)


    def write_i2c_block_data(self, i2c_addr, register, data, force = None):
        self._set_address(i2c_addr)
        self.write_to(register, data)


    def i2c_rdwr(self, *i2c_msgs):
        raise NotImplementedError()
