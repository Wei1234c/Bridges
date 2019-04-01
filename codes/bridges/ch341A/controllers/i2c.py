from array import array

import pyftdi.i2c
import usb
from pyftdi.i2c import I2cIOError, I2cNackError, hexlify, getLogger

from bridges.ch341A import CH341A



class I2cControllerBase:

    def __init__(self, device):
        self._device = device


    def _set_frequency(self, freq):
        self._device.set_i2c_speed(freq / 1000)
        return freq


    # def _commands_to_bytes(self, command, head = [CH341A.PORT.I2C], tail = [CH341A.I2C.COMMAND.END]):
    #     buf = head.copy()
    #     buf.extend(command)
    #     buf.extend(tail)
    #     return usb._interop.as_array(buf)
    #
    # def set_speed(self, speed_KHz = 400):
    #     self._device.set_i2c_speed(speed_KHz)
    #
    #
    # def _addr_for_write(self, addr, _10bits_addr = False):
    #     if _10bits_addr:
    #         addr = self._10bits_addr_to_bytes(addr)
    #         addr[0] = ((addr[0] << 1) | 0x00) & 0xFF
    #     else:
    #         addr = ((addr << 1) | 0x00) & 0xFF
    #     return addr
    #
    #
    # def _addr_for_read(self, addr, _10bits_addr = False):
    #     if _10bits_addr:
    #         addr = self._10bits_addr_to_bytes(addr)
    #         addr[0] = ((addr[0] << 1) | 0x01) & 0xFF
    #     else:
    #         addr = ((addr << 1) | 0x01) & 0xFF
    #     return addr
    #
    #
    # def _10bits_addr_to_bytes(self, addr):
    #     byte_h = 0x78 | (addr >> 8)
    #     byte_l = addr & 0xFF
    #     return _interop.as_array([byte_h, byte_l])
    #
    #
    # def _write_commands(self, commands):
    #     self._device.bulk_write(self._commands_to_bytes(commands))
    #
    #
    # def _cmd_write(self, buf):
    #     buf = _interop.as_array(buf)
    #     return [CH341A.I2C.COMMAND.OUT | len(buf), buf]
    #
    #
    # def _cmd_write(self, buf):
    #     buf = buf if hasattr(buf, '__len__') else [buf]
    #     cmd = [CH341A.I2C.COMMAND.OUT | len(buf)]
    #     cmd.extend(buf)
    #     return cmd
    #
    #
    # def _concat_commands(self, commands):
    #     cmd = []
    #     for command in commands:
    #         if hasattr(command, '__len__'):
    #             cmd.extend(command)
    #         else:
    #             cmd.appen(command)
    #     return cmd
    #
    #
    # def write_one_byte(self, byte):
    #     self._write_commands(self._cmd_write(byte))

    def _check_ACK(self):
        value = self._device.bulk_read(CH341A.ENDPOINTS.MAX_PACKET_SIZE.BULK_IN)
        return CH341A.I2C.RESPONSE.is_ACK(value)


    def _do_start(self):
        self.log.debug('   start')
        cmd = array('B', self._idle)
        cmd.extend(self._start)
        cmd.extend(self._immediate)
        self._device.write_data(cmd)


    def _do_stop(self):
        self._do_epilog()


    def _do_ack(self):
        self._write_one_byte(CH341A.I2C.RESPONSE.ACK)


    def _do_nack(self):
        self._write_one_byte(CH341A.I2C.RESPONSE.NACK)


    # def write_addr_for_write(self, addr, _10bits_addr = False):
    #     addr = self._addr_for_write(addr, _10bits_addr)
    #     self._write_commands([self._start, self._cmd_write(addr)])
    #
    #
    # def write_addr_for_read(self, addr, _10bits_addr = False):
    #     self.start()
    #     addr = self._addr_for_read(addr, _10bits_addr)
    #     self.write(addr) if _10bits_addr else self.write_one_byte(addr)

    def batch_read(self, length, buf = None):
        n_bytes_received = 0
        buf = usb.util.create_buffer(length) if buf is None else buf

        while length > n_bytes_received:
            n_bytes_to_receive = length - n_bytes_received
            n_bytes_to_receive = CH341A.I2C.PACKET.MAX_LENGTH if n_bytes_to_receive > CH341A.I2C.PACKET.MAX_LENGTH else n_bytes_to_receive

            self._device.bulk_write([CH341A.PORT.I2C,
                                     CH341A.I2C.COMMAND.IN | n_bytes_to_receive,
                                     CH341A.I2C.COMMAND.END])

            buf[n_bytes_received: n_bytes_received + n_bytes_to_receive] = self._device.bulk_read(n_bytes_to_receive)
            n_bytes_received += n_bytes_to_receive

        self._do_nack()
        self._do_stop()
        return buf


    # def readinto(self, buf, nack = True):
    #     buf = self.read_block(length = len(buf), buf = buf)
    #     if nack:
    #         self.nack()
    #     return buf

    # def readfrom_into(self, addr, buf, stop = True, _10bits_addr = False):
    #     self.write_addr_for_read(addr, _10bits_addr)
    #     buf = self.readinto(buf)
    #     if stop:
    #         self.stop()
    #     return buf

    # def readfrom(self, addr, nbytes, stop = True, _10bits_addr = False):
    #     buf = usb.util.create_buffer(nbytes)
    #     return self.readfrom_into(addr, buf, stop, _10bits_addr)

    def batch_write(self, buf):
        buf = buf if hasattr(buf, '__len__') else [buf]
        length = len(buf)
        n_bytes_sent = 0

        while length > n_bytes_sent:
            n_bytes_to_send = length - n_bytes_sent
            n_bytes_to_send = CH341A.I2C.PACKET.MAX_LENGTH if n_bytes_to_send > CH341A.I2C.PACKET.MAX_LENGTH else n_bytes_to_send
            cmd = [CH341A.PORT.I2C]
            cmd.extend([CH341A.I2C.COMMAND.OUT | n_bytes_to_send])
            cmd.extend(buf[n_bytes_sent: n_bytes_sent + n_bytes_to_send])
            cmd.extend([CH341A.I2C.DELAY.US | 10])
            cmd.extend([CH341A.I2C.COMMAND.END])

            self._device.bulk_write(cmd)
            n_bytes_sent += n_bytes_to_send

        self._do_stop()

    # def writeto(self, addr, buf, stop = True, _10bits_addr = False):
    #     self.write_addr_for_write(addr, _10bits_addr)
    #     self.write(buf)
    #     if stop:
    #         self.stop()

    # def readfrom_mem_into(self, addr, memaddr, buf, addrsize = 8):
    #     _10bits_addr = addrsize == 10
    #     self.write_addr_for_write(addr, _10bits_addr)
    #     self.write_one_byte(memaddr)
    #     return self.readfrom_into(addr, buf, stop = True, _10bits_addr = _10bits_addr)

    # def readfrom_mem(self, addr, memaddr, nbytes, addrsize = 8):
    #     buf = usb.util.create_buffer(nbytes)
    #     return self.readfrom_mem_into(addr, memaddr, buf, addrsize)
    #
    #
    # def writeto_mem(self, addr, memaddr, buf, addrsize = 8):
    #     _10bits_addr = addrsize == 10
    #     self.write_addr_for_write(addr, addrsize == 10)
    #     self.write_one_byte(memaddr)
    #     self.writeto(addr, buf, stop = True, _10bits_addr = _10bits_addr)



class I2cController(I2cControllerBase, pyftdi.i2c.I2cController):

    def __init__(self, device, **kwargs):
        I2cControllerBase.__init__(self, device)

        self.log = getLogger('ch341.controller.i2c')
        self._slaves = {}
        self._retry_count = self.RETRY_COUNT
        self._frequency = 0.0
        # self._direction = self.SCL_BIT | self.SDA_O_BIT
        # self._immediate = (Ftdi.SEND_IMMEDIATE,)
        # self._idle = (Ftdi.SET_BITS_LOW, self.IDLE, self._direction)
        # self._data_lo = (Ftdi.SET_BITS_LOW,
        #                  self.IDLE & ~self.SDA_O_BIT, self._direction)
        # self._clk_lo_data_lo = (Ftdi.SET_BITS_LOW,
        #                         self.IDLE & ~(self.SDA_O_BIT | self.SCL_BIT),
        #                         self._direction)
        # self._clk_lo_data_hi = (Ftdi.SET_BITS_LOW,
        #                         self.IDLE & ~self.SCL_BIT,
        #                         self._direction)
        # self._read_bit = (Ftdi.READ_BITS_PVE_MSB, 0)
        # self._read_byte = (Ftdi.READ_BYTES_PVE_MSB, 0, 0)
        self._immediate = (CH341A.I2C.COMMAND.END,)
        self._idle = (CH341A.PORT.I2C,)
        self._write_byte = (CH341A.I2C.COMMAND.OUT,)
        # self._nack = (Ftdi.WRITE_BITS_NVE_MSB, 0, self.HIGH)
        # self._ack = (Ftdi.WRITE_BITS_NVE_MSB, 0, self.LOW)
        self._ck_delay = 1
        self._start = None
        self._stop = None
        self._tristate = None
        self._tx_size = 1
        self._rx_size = 1

        self.configure(url = None, **kwargs)


    def _compute_delay_cycles(self, value):
        # approx ceiling without relying on math module
        # the bit delay is far from being precisely known anyway
        bit_delay = self._device.MPSSE_BIT_DELAY
        return max(1, int((value + bit_delay) / bit_delay))


    def configure(self, url, **kwargs):
        for k in ('direction', 'initial'):
            if k in kwargs:
                del kwargs[k]
        if 'frequency' in kwargs:
            frequency = kwargs['frequency']
            del kwargs['frequency']
        else:
            frequency = self.DEFAULT_BUS_FREQUENCY
        # Fix frequency for 3-phase clock
        if frequency <= 100E3:
            timings = self.I2C_100K
        elif frequency <= 400E3:
            timings = self.I2C_100K
        else:
            timings = self.I2C_100K
        if 'clockstretching' in kwargs:
            clkstrch = bool(kwargs['clockstretching'])
            del kwargs['clockstretching']
        else:
            clkstrch = False
        ck_hd_sta = self._compute_delay_cycles(timings.t_hd_sta)
        ck_su_sta = self._compute_delay_cycles(timings.t_su_sta)
        ck_su_sto = self._compute_delay_cycles(timings.t_su_sto)
        ck_buf = self._compute_delay_cycles(timings.t_buf)
        ck_idle = max(ck_su_sta, ck_buf)

        self._start = (CH341A.I2C.COMMAND.STA,)
        self._stop = (CH341A.I2C.COMMAND.STO,)

        self._ck_delay = ck_buf

        frequency = (3.0 * frequency) / 2.0
        self._frequency = self._set_frequency(frequency)
        self._tx_size, self._rx_size = self._device.fifo_sizes
        # self._device.enable_adaptive_clock(clkstrch)
        # self._device.enable_3phase_clock(True)
        # try:
        #     self._device.enable_drivezero_mode(self.SCL_BIT |
        #                                        self.SDA_O_BIT |
        #                                        self.SDA_I_BIT)
        # except FtdiFeatureError:
        #     self._tristate = (Ftdi.SET_BITS_LOW, self.LOW, self.SCL_BIT)


    def terminate(self):
        """Close the I2C interface.
        """
        if self._device:
            self._device.close()
            self._device = None


    @property
    def configured(self):
        return bool(self._device)


    # @property
    # def frequency_max(self):
    #     """Provides the maximum I2c clock frequency.
    #     """
    #     return self._device.frequency_max

    #
    # @property
    # def frequency(self):
    #     """Provides the current I2c clock frequency.
    #
    #        :return: the I2C bus clock
    #        :rtype: float
    #     """
    #     return self._frequency

    def _prepare_address(self, address, to_write = True):
        if not self.configured:
            raise I2cIOError("I2C controller not initialized")
        self.validate_address(address)
        if address is None:
            i2caddress = None
        else:
            i2caddress = (address << 1) & self.HIGH | (0x00 if to_write else self.BIT0)
        return i2caddress


    def read(self, address, readlen = 1, relax = True):
        i2caddress = self._prepare_address(address, to_write = True)
        retries = self._retry_count
        do_epilog = True
        while True:
            try:
                self._do_prolog(i2caddress)
                data = self._do_read(readlen)
                do_epilog = relax
                return data
            except I2cNackError:
                retries -= 1
                if not retries:
                    raise
                self.log.warning('Retry read')
            finally:
                if do_epilog:
                    self._do_epilog()


    def write(self, address, out, relax = True):
        i2caddress = self._prepare_address(address, to_write = True)

        retries = self._retry_count
        do_epilog = True
        while True:
            try:
                self._do_prolog(i2caddress)
                self._do_write(out)
                # I2cControllerBase.batch_write(self, out)
                do_epilog = relax
                return
            except I2cNackError:
                retries -= 1
                if not retries:
                    raise
                self.log.warning('Retry write')
            finally:
                if do_epilog:
                    self._do_epilog()


    def exchange(self, address, out, readlen = 0, relax = True):
        """Send a byte sequence to a remote slave followed with
           a read request of one or more bytes.

           This command is useful to tell the slave what data
           should be read out.

           :param address: the address on the I2C bus, or None to discard start
           :type address: int or None
           :param out: the byte buffer to send
           :type out: array or bytes or list(int)
           :param int readlen: count of bytes to read out.
           :param bool relax: whether to relax the bus (emit STOP) or not
           :return: read bytes
           :rtype: array
           :raise I2cIOError: if device is not configured or input parameters
                              are invalid

           Address is a logical slave address (0x7f max)
        """

        if readlen < 1:
            raise I2cIOError('Nothing to read')
        if readlen > (I2cController.PAYLOAD_MAX_LENGTH / 3 - 1):
            raise I2cIOError("Input payload is too large")

        i2caddress = self._prepare_address(address, to_write = True)

        retries = self._retry_count
        do_epilog = True
        while True:
            try:
                self._do_prolog(i2caddress)
                self._do_write(out)
                self._do_prolog(i2caddress | self.BIT0)
                if readlen:
                    data = self._do_read(readlen)
                do_epilog = relax
                return data
            except I2cNackError:
                retries -= 1
                if not retries:
                    raise
                self.log.warning('Retry exchange')
            finally:
                if do_epilog:
                    self._do_epilog()


    def poll(self, address, write = False, relax = False):
        i2caddress = self._prepare_address(address, to_write = True)

        do_epilog = True
        try:
            self._do_prolog(i2caddress)
            do_epilog = relax
            return True

        except I2cNackError:
            return False

        finally:
            if do_epilog:
                self._do_epilog()


    # def poll_cond(self, address, fmt, mask, value, count, relax = True):
    #     """Poll a remove slave, watching for condition to satisfy.
    #        On each poll cycle, a repeated start condition is emitted, without
    #        releasing the I2C bus, and an ACK is returned to the slave.
    #
    #        If relax is set, this method releases the I2C bus however it leaves.
    #
    #        :param address: the address on the I2C bus, or None to discard start
    #        :type address: int or None
    #        :param str fmt: struct format for poll register
    #        :param int mask: binary mask to apply on the condition register
    #             before testing for the value
    #        :param int value: value to t the masked condition register
    #             against. Condition is satisfied when register & mask == value
    #        :param int count: maximum poll count before raising a timeout
    #        :param bool relax: whether to relax the bus (emit STOP) or not
    #        :return: the polled register value, or None if poll failed
    #        :rtype: array or None
    #     """
    #     i2caddress = self._prepare_address(address, to_write = True)
    #     do_epilog = True
    #     try:
    #         retry = 0
    #         while retry < count:
    #             retry += 1
    #             size = scalc(fmt)
    #             self._do_prolog(i2caddress)
    #             data = self._do_read(size)
    #             self.log.debug("Poll data: %s", hexlify(data).decode())
    #             cond, = sunpack(fmt, data)
    #             if (cond & mask) == value:
    #                 self.log.debug('Poll condition matched')
    #                 break
    #             else:
    #                 data = None
    #                 self.log.debug('Poll condition not fulfilled: %x/%x',
    #                                cond & mask, value)
    #         do_epilog = relax
    #         if not data:
    #             self.log.warning('Poll condition failed')
    #         return data
    #     except I2cNackError:
    #         self.log.info('Not ready')
    #         return None
    #     finally:
    #         if do_epilog:
    #             self._do_epilog()

    # def flush(self):
    #     """Flush the HW FIFOs
    #     """
    #     if not self.configured:
    #         raise I2cIOError("I2C controller not initialized")
    #     self._device.write_data(self._immediate)
    #     self._device.purge_buffers()

    def _do_prolog(self, i2caddress):
        if i2caddress is None:
            return
        self.log.debug('   prolog 0x%x', i2caddress >> 1)
        cmd = array('B', self._idle)
        cmd.extend(self._start)
        cmd.extend(self._write_byte)
        cmd.append(i2caddress)
        # if self._tristate:
        #     cmd.extend(self._tristate)
        #     cmd.extend(self._read_bit)
        #     cmd.extend(self._clk_lo_data_hi)
        # else:
        #     cmd.extend(self._clk_lo_data_hi)
        #     cmd.extend(self._read_bit)
        cmd.extend(self._immediate)
        self._device.write_data(cmd)
        value = self._device.read_data_bytes(1, 4)

        if not value:
            raise I2cIOError('No answer from slave')
        if CH341A.I2C.RESPONSE.is_NACK(value):
            raise I2cNackError('NACK from slave')


    def _do_epilog(self):
        self.log.debug('   epilog')
        cmd = array('B', self._idle)
        cmd.extend(self._stop)
        cmd.extend(self._immediate)
        self._device.write_data(cmd)


    def _write_one_byte(self, byte):
        cmd = array('B', self._idle)
        cmd.extend([CH341A.I2C.COMMAND.OUT | 1])
        cmd.append(byte)
        cmd.extend(self._immediate)
        self._device.write_data(cmd)


    def _do_read(self, readlen):
        self.log.debug('- read %d byte(s)', readlen)
        if not readlen:
            # force a real read request on device, but discard any result
            cmd = array('B', self._idle)
            cmd.extend(self._immediate)
            self._device.write_data(cmd)
            self._device.read_data_bytes(0, 4)
            return array('B')
        if self._tristate:
            read_byte = self._tristate + \
                        self._read_byte + \
                        self._clk_lo_data_hi
            read_not_last = \
                read_byte + self._ack + self._clk_lo_data_lo * self._ck_delay
            read_last = \
                read_byte + self._nack + self._clk_lo_data_hi * self._ck_delay
        else:
            read_not_last = \
                self._read_byte + self._ack + \
                self._clk_lo_data_hi * self._ck_delay
            read_last = \
                self._read_byte + self._nack + \
                self._clk_lo_data_hi * self._ck_delay
        # maximum RX size to fit in I2C FIFO, minus 2 status bytes
        chunk_size = self._rx_size - 2
        cmd_size = len(read_last)
        # limit RX chunk size to the count of I2C packable commands in the I2C
        # TX FIFO (minus one byte for the last 'send immediate' command)
        tx_count = (self._tx_size - 1) // cmd_size
        chunk_size = min(tx_count, chunk_size)
        chunks = []
        cmd = None
        rem = readlen
        while rem:
            if rem > chunk_size:
                if not cmd:
                    cmd = array('B')
                    cmd.extend(read_not_last * chunk_size)
                    size = chunk_size
            else:
                cmd = array('B')
                cmd.extend(read_not_last * (rem - 1))
                cmd.extend(read_last)
                cmd.extend(self._immediate)
                size = rem
            self._device.write_data(cmd)
            buf = self._device.read_data_bytes(size, 4)
            self.log.debug('- read %d byte(s): %s',
                           len(buf), hexlify(buf).decode())
            chunks.append(buf)
            rem -= size
        return array('B', b''.join(chunks))


    def _do_write(self, out):
        if not isinstance(out, array):
            out = array('B', out)
        if not out:
            return
        self.log.debug('- write %d byte(s): %s',
                       len(out), hexlify(out).decode())
        for byte in out:
            cmd = array('B', self._idle)
            cmd.extend(self._write_byte)
            cmd.append(byte)
            # if self._tristate:
            #     cmd.extend(self._tristate)
            #     cmd.extend(self._read_bit)
            #     cmd.extend(self._clk_lo_data_hi)
            # else:
            #     cmd.extend(self._clk_lo_data_hi)
            #     cmd.extend(self._read_bit)
            cmd.extend(self._immediate)
            self._device.write_data(cmd)
            value = self._device.read_data_bytes(1, 4)
            if not value:
                msg = 'No answer from slave'
                self.log.critical(msg)
                raise I2cIOError(msg)
            if CH341A.I2C.RESPONSE.is_NACK(value):
                raise I2cNackError('NACK from slave')



class I2cPort(pyftdi.i2c.I2cPort):
    """
    redirect functional requests to I2cController.
    """
