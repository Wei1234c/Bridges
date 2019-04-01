import pyftdi.spi
import usb
from usb import _interop

from bridges.ch341A import CH341A



class SpiPort(pyftdi.spi.SpiPort):

    def __init__(self, device):
        self.device = device
        self.set_speed()
        # self.stop()


    def set_speed(self, speed_KHz = 400):
        self.device.set_i2c_speed(speed_KHz)


    def _addr_for_write(self, addr, _10bits_addr = False):
        if _10bits_addr:
            addr = self._10bits_addr_to_bytes(addr)
            addr[0] = ((addr[0] << 1) | 0x00) & 0xFF
        else:
            addr = ((addr << 1) | 0x00) & 0xFF
        return addr


    def _addr_for_read(self, addr, _10bits_addr = False):
        if _10bits_addr:
            addr = self._10bits_addr_to_bytes(addr)
            addr[0] = ((addr[0] << 1) | 0x01) & 0xFF
        else:
            addr = ((addr << 1) | 0x01) & 0xFF
        return addr


    def _10bits_addr_to_bytes(self, addr):
        byte_h = 0x78 | (addr >> 8)
        byte_l = addr & 0xFF
        return _interop.as_array([byte_h, byte_l])


    def start(self):
        self.device.bulk_write([CH341A.PORT.I2C,
                                CH341A.I2C.COMMAND.STA,
                                CH341A.I2C.COMMAND.END])


    def stop(self):
        self.device.bulk_write([CH341A.PORT.I2C,
                                CH341A.I2C.COMMAND.STO,
                                CH341A.I2C.COMMAND.END])


    def ack(self):
        self.write_one_byte(CH341A.I2C.RESPONSE.ACK)


    def nack(self):
        self.write_one_byte(CH341A.I2C.RESPONSE.NACK)


    def write_one_byte(self, byte):
        self.device.bulk_write([CH341A.PORT.I2C,
                                CH341A.I2C.COMMAND.OUT | 1,
                                byte,
                                CH341A.I2C.COMMAND.END])


    def _check_ACK(self):
        value = self.device.bulk_read(CH341A.ENDPOINTS.MAX_PACKET_SIZE.BULK_IN)
        return CH341A.I2C.RESPONSE.is_ACK(value)


    def write_addr_for_write(self, addr, _10bits_addr = False):
        self.start()
        addr = self._addr_for_write(addr, _10bits_addr)
        self.write(addr) if _10bits_addr else self.write_one_byte(addr)


    def write_addr_for_read(self, addr, _10bits_addr = False):
        self.start()
        addr = self._addr_for_read(addr, _10bits_addr)
        self.write(addr) if _10bits_addr else self.write_one_byte(addr)


    def check_addr(self, addr):
        self.start()
        self.device.bulk_write([CH341A.PORT.I2C,
                                CH341A.I2C.COMMAND.OUT,
                                addr,
                                CH341A.I2C.COMMAND.END])
        self.stop()
        return self._check_ACK()


    def scan_i2c_bus(self, n_addr = 128):
        addrs = [addr for addr in range(n_addr) if self.check_addr(self._addr_for_write(addr))]
        print("Found devices at:", [hex(addr) for addr in addrs])
        return addrs


    def read_block(self, length, buf = None):
        n_bytes_received = 0
        buf = usb.util.create_buffer(length) if buf is None else buf

        while length > n_bytes_received:
            n_bytes_to_receive = length - n_bytes_received
            n_bytes_to_receive = CH341A.I2C.PACKET.MAX_LENGTH \
                if n_bytes_to_receive > CH341A.I2C.PACKET.MAX_LENGTH \
                else n_bytes_to_receive

            self.device.bulk_write(
                [CH341A.PORT.I2C,
                 CH341A.I2C.COMMAND.IN | n_bytes_to_receive,
                 CH341A.I2C.COMMAND.END])
            buf[n_bytes_received: n_bytes_received + n_bytes_to_receive] = self.device.bulk_read(n_bytes_to_receive)
            n_bytes_received += n_bytes_to_receive

        return buf


    # # bridges.interfaces.micropython.machine.I2C
    # def __init__(self, id, scl, sda, freq = 400000):
    #     raise NotImplementedError()

    def init(self, scl, sda, freq = 400000):
        self.set_speed(freq // 1000)


    def deinit(self):
        print('Not Applicable.')


    def scan(self):
        return self.scan_i2c_bus()


    def readinto(self, buf, nack = True):
        buf = self.read_block(length = len(buf), buf = buf)
        if nack:
            self.nack()
        return buf


    def readfrom_into(self, addr, buf, stop = True, _10bits_addr = False):
        self.write_addr_for_read(addr, _10bits_addr)
        buf = self.readinto(buf)
        if stop:
            self.stop()
        return buf


    def readfrom(self, addr, nbytes, stop = True, _10bits_addr = False):
        buf = usb.util.create_buffer(nbytes)
        return self.readfrom_into(addr, buf, stop, _10bits_addr)


    def write(self, buf):
        length = len(buf)
        n_bytes_sent = 0

        while length > n_bytes_sent:
            n_bytes_to_send = length - n_bytes_sent
            n_bytes_to_send = CH341A.I2C.PACKET.MAX_LENGTH \
                if n_bytes_to_send > CH341A.I2C.PACKET.MAX_LENGTH\
                else n_bytes_to_send

            data = [CH341A.PORT.I2C, CH341A.I2C.COMMAND.OUT | n_bytes_to_send]
            data.extend(buf[n_bytes_sent: n_bytes_sent + n_bytes_to_send])
            data.extend([CH341A.I2C.COMMAND.END])

            self.device.bulk_write(data)
            n_bytes_sent += n_bytes_to_send


    def writeto(self, addr, buf, stop = True, _10bits_addr = False):
        self.write_addr_for_write(addr, _10bits_addr)
        self.write(buf)
        if stop:
            self.stop()


    def readfrom_mem_into(self, addr, memaddr, buf, addrsize = 8):
        _10bits_addr = addrsize == 10
        self.write_addr_for_write(addr, _10bits_addr)
        self.write_one_byte(memaddr)
        return self.readfrom_into(addr, buf, stop = True, _10bits_addr = _10bits_addr)


    def readfrom_mem(self, addr, memaddr, nbytes, addrsize = 8):
        buf = usb.util.create_buffer(nbytes)
        return self.readfrom_mem_into(addr, memaddr, buf, addrsize)


    def writeto_mem(self, addr, memaddr, buf, addrsize = 8):
        _10bits_addr = addrsize == 10
        self.write_addr_for_write(addr, addrsize == 10)
        self.write_one_byte(memaddr)
        self.writeto(addr, buf, stop = True, _10bits_addr = _10bits_addr)
