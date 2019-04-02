I2C_SMBUS_BLOCK_MAX = 32
HIGHEST_I2C_ADDRESS = 0x78



class SMBus:

    def __init__(self, bus = None, force = False):
        raise NotImplementedError()


    def open(self, bus):
        raise NotImplementedError()


    def close(self):
        raise NotImplementedError()


    def _set_address(self, address, force = None):
        raise NotImplementedError()


    def _get_funcs(self):
        raise NotImplementedError()


    def write_quick(self, i2c_addr, force = None):
        raise NotImplementedError()


    def read_byte(self, i2c_addr, force = None):
        raise NotImplementedError()


    def write_byte(self, i2c_addr, value, force = None):
        raise NotImplementedError()


    def read_byte_data(self, i2c_addr, register, force = None):
        raise NotImplementedError()


    def write_byte_data(self, i2c_addr, register, value, force = None):
        raise NotImplementedError()


    def read_word_data(self, i2c_addr, register, force = None):
        raise NotImplementedError()


    def write_word_data(self, i2c_addr, register, value, force = None):
        raise NotImplementedError()


    def process_call(self, i2c_addr, register, value, force = None):
        raise NotImplementedError()


    def read_block_data(self, i2c_addr, register, force = None):
        raise NotImplementedError()


    def write_block_data(self, i2c_addr, register, data, force = None):
        raise NotImplementedError()


    def block_process_call(self, i2c_addr, register, data, force = None):
        raise NotImplementedError()


    def read_i2c_block_data(self, i2c_addr, register, length, force = None):
        raise NotImplementedError()


    def write_i2c_block_data(self, i2c_addr, register, data, force = None):
        raise NotImplementedError()


    def i2c_rdwr(self, *i2c_msgs):
        raise NotImplementedError()
