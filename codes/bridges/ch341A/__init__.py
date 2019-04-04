import struct

from bridges.universal_serial_bus import *


CH341_PACKET_LENGTH_MAX = 32



class CommandStream:

    def __init__(self, commands = [], head = [], tail = []):
        self.init_commands(commands)
        self._head = head
        self._tail = tail


    def init_commands(self, commands):
        commands = commands if hasattr(commands, '__len__') else [commands]
        self.commands = commands
        return self


    def clear(self):
        self.commands = []
        return self


    def extend(self, commands):
        commands = commands if hasattr(commands, '__len__') else [commands]
        self.commands.extend(commands)
        return self


    def append(self, command, param = 0x00):
        self.commands.append(command | param)
        return self


    @property
    def buffer(self):
        buf = self._head.copy()
        buf.extend(self.commands)
        buf.extend(self._tail)
        return buf


    @property
    def bytes(self):
        return usb._interop.as_array(self.buffer)



class I2cCommands(CommandStream):

    def __init__(self, commands = []):
        super().__init__(commands = commands,
                         head = [CH341A.PORT.I2C],
                         tail = [CH341A.I2C.COMMAND.END])



class CH341A(USBdevice):
    ID_VENDOR = 0x1a86
    TYPE = CONTROL_REQUEST.TYPE.VENDOR
    DEFAULT_INTERFACE = (0, 0)
    MODES = {'Synchronous_Serial': {'idProduct': 0x5512}, 'UART': {'idProduct': 0x5523},
             'Printer'           : {'idProduct': 0x5584}, 'Parallel': {'idProduct': None}}
    MAX_NUMBER = 16  # 最多同时连接的CH341数
    MAX_BUFFER_LENGTH = 0x1000  # 数据缓冲区最大长度4096
    DEFAULT_BUFFER_LEN = 0x0400  # 数据缓冲区默认长度1024
    MPSSE_BIT_DELAY = 0.5E-6


    class ENDPOINTS:
        BULK_IN = 0x82
        BULK_OUT = 0x02
        INTERRUPT_IN = 0x81
        INTERRUPT_OUT = 0x01


        class MAX_PACKET_SIZE:
            BULK_IN = 32
            BULK_OUT = 32
            INTERRUPT_IN = 8
            INTERRUPT_OUT = 8


    class PACKET_SIZE:
        LENGTH_MAX = 32  # CH341支持的数据包的长度
        LENGTH_SHORT = 8  # CH341支持的短数据包的长度


    class PORT:
        READ_REG = 0x95
        WRITE_REG = 0x9A
        SERIAL = 0xA1
        SET_OUTPUT = 0xA1  # Set Para Output  # 设置并口输出
        IO_ADDR = 0xA2  # MEM Addr write/read  # MEM带地址读写/输入输出,从次字节开始为命令流
        PRINTER = 0xA3  # Print output  # PRINT兼容打印方式输出,从次字节开始为数据流
        PWM = 0xA4  # PWM Out Command  # PWM数据输出的命令包,从次字节开始为数据流
        MODEM = 0xA4
        SHORT_PKT = 0xA5  # short package  # 短包,次字节是该命令包的真正长度,再次字节及之后的字节是原命令包
        MEMW = 0xA6  # aka mCH341_PARA_CMD_W0
        MEMR = 0xAC  # aka mCH341_PARA_CMD_R0
        SPI = 0xA8  # SPI Interface Command  # SPI接口的命令包,从次字节开始为数据流
        SIO = 0xA9  # SIO接口的命令包,从次字节开始为数据流
        I2C = 0xAA  # I2C Interface Command  # I2C接口的命令包,从次字节开始为I2C命令流
        UIO = 0xAB  # UIO Interface Command  # UIO接口的命令包,从次字节开始为命令流
        PIO = 0xAE  # PIO Interface Command  # PIO接口的命令包,从次字节开始为数据流


    class REQUEST:
        # CH341控制传输的厂商专用请求代码
        PARA_INIT = 0xB1  # Init para  # 初始化并口
        GET_STATUS = 0x52  # Get I2C Interface State  # 获取I2C接口的状态
        I2C_COMMAND = 0x53  # Send I2C Command  # 发出I2C接口的命令

        # CH341A控制传输的厂商专用请求代码
        BUF_CLEAR = 0xB2  # clear uncompleted data  # 清除未完成的数据
        I2C_CMD_X = 0x54  # Send I2C Interface command  # 发出I2C接口的命令,立即执行
        DELAY_MS = 0x5E  # Set Delay(ms)  # 以亳秒为单位延时指定时间
        GET_VERSION = 0x5F  # Get Chip Version  # 获取芯片版本


    class I2C:
        class COMMAND:
            STA = 0x74  # I2C Stream Start Command  # I2C接口的命令流:产生起始位
            STO = 0x75  # I2C Stream Stop byte Command  # I2C接口的命令流:产生停止位
            OUT = 0x80  # I2C Stream Out Command  # I2C接口的命令流:输出数据,位5-位0为长度,后续字节为数据,0长度则只发送一个字节并返回
            IN = 0xC0  # I2C Stream In Command  # I2C接口的命令流:输入数据,位5-位0为长度,0长度则只接收一个字节并发送无应答
            SET = 0x60  # I2C Stream Set Mode  # I2C接口的命令流:设置参数,位2=SPI的I/O数(0=单入单出,1=双入双出),位1位0=I2C速度(00=低速,01=标准,10=快速,11=高速)
            END = 0x00  # I2C Stream End Command  # I2C接口的命令流:命令包提前结束


        class PACKET:
            # I2C Stream Max Length  # I2C接口的命令流单个命令输入输出数据的最大长度
            MAX_LENGTH = min(0x3F, CH341_PACKET_LENGTH_MAX)


        class RESPONSE:
            MASK = 0X80
            ACK = 0x00
            NACK = 0x80


            @staticmethod
            def is_ACK(value):
                assert (len(value) == 1)
                return (value[0] & CH341A.I2C.RESPONSE.MASK) == CH341A.I2C.RESPONSE.ACK


            @staticmethod
            def is_NACK(value):
                assert (len(value) == 1)
                return (value[0] & CH341A.I2C.RESPONSE.MASK) == CH341A.I2C.RESPONSE.NACK


        class DELAY:
            US = 0x40  # I2C Stream Delay(us)  # I2C接口的命令流:以微秒为单位延时,位3-位0为延时值
            MS = 0x50  # I2C Stream Delay(ms)  # I2C接口的命令流:以亳秒为单位延时,位3-位0为延时值
            MAX_DLY = 0x0F  # I2C Stream Set Max Delay  # I2C接口的命令流单个命令延时的最大值


        class SPEED:
            STANDARD_MODE = 100
            FAST_MODE = 400
            FAST_MODE_PLUS = 1024
            HIGH_SPEED_MODE = 3.4 * FAST_MODE_PLUS


            # 位1-位0: I2C接口速度/SCL频率, 00=低速/20KHz,01=标准/100KHz(默认值),10=快速/400KHz,11=高速/750KHz
            @staticmethod
            def get_speed_id(speed_KHz):
                mode = 0x03
                if speed_KHz < 100:
                    mode = 0x00
                elif speed_KHz < 400:
                    mode = 0x01
                elif speed_KHz < 750:
                    mode = 0x02
                return mode


    class PARALLEL:
        # CH341并口工作模式
        class MODE:
            EPP = 0x00  # CH341并口工作模式为EPP方式
            EPP17 = 0x00  # CH341A并口工作模式为EPP方式V1.7
            EPP19 = 0x01  # CH341A并口工作模式为EPP方式V1.9
            MEM = 0x02  # CH341并口工作模式为MEM方式
            ECP = 0x03  # CH341A并口工作模式为ECP方式


        # CH341并口操作命令代码
        class COMMAND:
            R0 = 0xAC  # Read Data0 From Para  # 从并口读数据0,次字节为长度
            R1 = 0xAD  # Read Data1 From Para  # 从并口读数据1,次字节为长度
            W0 = 0xA6  # Write Data0 From Para  # 向并口写数据0,从次字节开始为数据流
            W1 = 0xA7  # Write Data1 From Para  # 向并口写数据1,从次字节开始为数据流
            STS = 0xA0  # Get Para State  # 获取并口状态


    class UIO:
        class COMMAND:
            IN = 0x00  # UIO Interface In ( D0 ~ D7 )  # UIO接口的命令流:输入数据D7-D0
            DIR = 0x40  # UIO interface Dir( set dir of D0~D5 )  # UIO接口的命令流:设定I/O方向D5-D0,位5-位0为方向数据
            OUT = 0x80  # UIO Interface Output(D0~D5)  # UIO接口的命令流:输出数据D5-D0,位5-位0为数据
            US = 0xC0  # UIO Interface Delay Command( us )  # UIO接口的命令流:以微秒为单位延时,位5-位0为延时值
            END = 0x20  # UIO Interface End Command  # UIO接口的命令流:命令包提前结束


    class PinState:
        bits_map = (('D0', 0), ('D1', 1), ('D2', 2), ('D3', 3), ('D4', 4), ('D5', 5), ('D6', 6), ('D7', 7), ('ERR', 8),
                    ('PEMP', 9), ('INT', 10), ('SLCT', 11), ('WAIT', 13), ('DATAS', 14), ('ADDRS', 15), ('RESET', 16),
                    ('WRITE', 17), ('SCL', 18), ('SDA', 29))


        def __init__(self, bits):

            if type(bits) != type(int):
                out = struct.unpack_from(">IH", bytearray(bits))
                bits = out[0]
            self.bits = bits


        @property
        def status(self):
            return {name: 1 if self.bits & (1 << pin) else 0 for name, pin in self.bits_map}


        def __str__(self):
            return 'Pins Status:\n' + ''.join(
                ['  {:<6}: {:>2}\n'.format(name, status) for name, status in self.status.items()])


    def __init__(self, address = None, mode = 'Synchronous_Serial'):
        super().__init__(vid = CH341A.ID_VENDOR, pid = CH341A.MODES[mode]['idProduct'], address = address)
        self.interrupt_read = self.endpoints[CH341A.ENDPOINTS.INTERRUPT_IN].read
        self.bulk_read = self.endpoints[CH341A.ENDPOINTS.BULK_IN].read
        self.stream_mode = 0x82
        self.frequency_max = CH341A.I2C.SPEED.FAST_MODE * 1000
        self.fifo_sizes = (CH341A.ENDPOINTS.MAX_PACKET_SIZE.BULK_OUT,
                           CH341A.ENDPOINTS.MAX_PACKET_SIZE.BULK_IN)
        self.max_packet_size = CH341A.ENDPOINTS.MAX_PACKET_SIZE.BULK_OUT
        self.write_data = self.bulk_write


    def read_data_bytes(self, size, attempt = 1):
        return self.bulk_read(size)


    def bulk_write(self, data):
        count = self.endpoints[CH341A.ENDPOINTS.BULK_OUT].write(data)
        assert count == len(data), "Failed writing to USB"
        return count


    def clear_buffers(self):
        self.control_write(CH341A.REQUEST.BUF_CLEAR)


    @property
    def version(self):
        version = self.control_read(CH341A.REQUEST.GET_VERSION, 0, 0, 2)
        return '{:d}.{:d}'.format(version[0], version[1])


    @property
    def status(self):
        status = self.control_read(CH341A.REQUEST.GET_STATUS, 0, 0, 6)
        return CH341A.PinState(status)


    def get_pin_status(self, pin):
        return self.status.status[pin]


    # /*
    #  * ********************************************************************
    #  * FUNCTION : Set Stream Mode
    #  * arg:
    #  * Mode : Set Stream Mode
    #  * -> bit0~1 : set I2C SCL rate
    #  * 			   --> 00 :	Low Rate /20KHz
    #  * 			   --> 01 : Default Rate /100KHz
    #  * 			   --> 10 : Fast Rate /400KHz
    #  * 			   --> 11 : Full Rate /750KHz
    #  * -> bit2 : set spi mode
    #  * 			   --> 0 : one in one out(D3 :clk/ D5 :out/ D7 :in)
    #  * 			   --> 1 : two in two out(D3 :clk/ D4,D5 :out/ D6,D7 :in)
    #  * -> bit7 : set spi data mode
    #  * 			   --> 0 : low bit first
    #  *       	       --> 1 : high bit first
    #  * other bits must keep 0
    #  * ********************************************************************
    #  */
    # # 设置串口流模式
    #   Mode    # 指定模式,见下行
    #           # 位1-位0: I2C接口速度/SCL频率, 00=低速/20KHz,01=标准/100KHz(默认值),10=快速/400KHz,11=高速/750KHz
    #           # 位2:     SPI的I/O数/IO引脚, 0=单入单出(D3时钟/D5出/D7入)(默认值),1=双入双出(D3时钟/D5出D4出/D7入D6入)
    #           # 位7:     SPI字节中的位顺序, 0=低位在前, 1=高位在前
    #           # 其它保留,必须为0
    def set_stream(self, mode):
        if float(self.version) < 0x20:
            return False
        self.bulk_write([CH341A.PORT.I2C,
                         CH341A.I2C.COMMAND.SET, mode,
                         CH341A.I2C.COMMAND.END])


    def _set_stream_mode(self, i2c_mode = None, spi_mode = None):
        i2c_mode = self.stream_mode & 0x03 if i2c_mode is None else i2c_mode & 0x03
        spi_mode = self.stream_mode & 0x84 if spi_mode is None else spi_mode & 0x84
        self.stream_mode = i2c_mode | spi_mode
        return self.stream_mode


    def set_i2c_speed(self, speed_KHz = 400):
        i2c_mode = CH341A.I2C.SPEED.get_speed_id(speed_KHz)
        stream_mode = self._set_stream_mode(i2c_mode = i2c_mode)
        self.set_stream(stream_mode)


    # /*
    #  * ********************************************************************
    #  * FUNCTION : Set Delay
    #  * arg:
    #  * iDelay : set delay time(ms)
    #  * ********************************************************************
    #  */
    # # 设置硬件异步延时,调用后很快返回,而在下一个流操作之前延时指定毫秒数
    #   iDelay      # 指定延时的毫秒数
    def set_delay_ms(self, iDelay):
        if float(self.version) < 0x20:
            return False

        while iDelay:
            mLength = CH341A.I2C.DELAY.MAX_DLY if iDelay >= CH341A.I2C.DELAY.MAX_DLY else iDelay
            iDelay -= mLength

            self.bulk_write([CH341A.PORT.I2C,
                             CH341A.I2C.DELAY.MS | mLength,
                             CH341A.I2C.COMMAND.END])
        return True


    # /*
    #  * ********************************************************************
    #  * FUNCTION : Set direction and output data of D5-D0 on CH341
    #  * arg:
    #  * Data : Control direction and data
    #  * iSetDirOut : set io direction
    #  *			  -- > Bit High : Output
    #  *			  -- > Bit Low : Input
    #  * iSetDataOut : set io data
    #  * 			 Output:
    #  *			  -- > Bit High : High level
    #  *			  -- > Bit Low : Low level
    #  * ********************************************************************
    #  */
    # # 设置CH341的D5-D0引脚的I/O方向,并通过CH341的D5-D0引脚直接输出数据,效率比CH341SetOutput更高
    # /* ***** 谨慎使用该API, 防止修改I/O方向使输入引脚变为输出引脚导致与其它输出引脚之间短路而损坏芯片 ***** */
    #   iSetDirOut      # 设置D5-D0各引脚的I/O方向,某位清0则对应引脚为输入,某位置1则对应引脚为输出,并口方式下默认值为0x00全部输入
    #   iSetDataOut     # 设置D5-D0各引脚的输出数据,如果I/O方向为输出,那么某位清0时对应引脚输出低电平,某位置1时对应引脚输出高电平
    #                   # 以上数据的位5-位0分别对应CH341的D5-D0引脚
    def set_D5_D0(self, iSetDirOut = 0x00, iSetDataOut = 0x00):
        MASK = 0x3F
        self.bulk_write(
            [CH341A.PORT.UIO,
             CH341A.UIO.COMMAND.OUT | iSetDataOut & MASK,
             CH341A.UIO.COMMAND.DIR | iSetDirOut & MASK,
             CH341A.UIO.COMMAND.END])


    # /*
    #  * ********************************************************************
    #  * FUNCTION : Set direction and output data of CH341
    #  * arg:
    #  * Data :	Control direction and data
    #
    #  * iEnbale : set direction and data enable
    #  * 			   --> Bit16 High :	effect on Bit15~8 of iSetDataOut
    #  * 			   --> Bit17 High :	effect on Bit15~8 of iSetDirOut
    #  * 			   --> Bit18 High :	effect on Bit7~0 of iSetDataOut
    #  * 			   --> Bit19 High :	effect on Bit7~0 of iSetDirOut
    #  *			   --> Bit20 High :	effect on Bit23~16 of iSetDataOut
    #  * iSetDirOut : set io direction
    #  *			  -- > Bit High : Output
    #  *			  -- > Bit Low : Input
    #  * iSetDataOut : set io data
    #  * 			 Output:
    #  *			  -- > Bit High : High level
    #  *			  -- > Bit Low : Low level
    #  * Note:
    #  * Bit7~Bit0<==>D7-D0
    #  * Bit8<==>ERR#    Bit9<==>PEMP    Bit10<==>INT#    Bit11<==>SLCT    Bit13<==>WAIT#    Bit14<==>DATAS#/READ#    Bit15<==>ADDRS#/ADDR/ALE
    #  * The pins below can only be used in output mode:
    #  * Bit16<==>RESET#    Bit17<==>WRITE#    Bit18<==>SCL    Bit29<==>SDA
    #  * ********************************************************************
    #  */
    # # 设置CH341的I/O方向,并通过CH341直接输出数据
    # /* ***** 谨慎使用该API, 防止修改I/O方向使输入引脚变为输出引脚导致与其它输出引脚之间短路而损坏芯片 ***** */
    #   iEnable     # 数据有效标志,参考下面的位说明
    #               # 位0为1说明iSetDataOut的位15-位8有效,否则忽略
    #               # 位1为1说明iSetDirOut的位15-位8有效,否则忽略
    #               # 位2为1说明iSetDataOut的7-位0有效,否则忽略
    #               # 位3为1说明iSetDirOut的位7-位0有效,否则忽略
    #               # 位4为1说明iSetDataOut的位23-位16有效,否则忽略
    #   iSetDirOut  # 设置I/O方向,某位清0则对应引脚为输入,某位置1则对应引脚为输出,并口方式下默认值为0x000FC000,参考下面的位说明
    #   iSetDataOut # 输出数据,如果I/O方向为输出,那么某位清0时对应引脚输出低电平,某位置1时对应引脚输出高电平,参考下面的位说明
    #               # 位7-位0对应CH341的D7-D0引脚
    #               # 位8对应CH341的ERR#引脚, 位9对应CH341的PEMP引脚, 位10对应CH341的INT#引脚, 位11对应CH341的SLCT引脚
    #               # 位13对应CH341的WAIT#引脚, 位14对应CH341的DATAS#/READ#引脚,位15对应CH341的ADDRS#/ADDR/ALE引脚
    #               # 以下引脚只能输出,不考虑I/O方向: 位16对应CH341的RESET#引脚, 位17对应CH341的WRITE#引脚, 位18对应CH341的SCL引脚, 位29对应CH341的SDA引脚
    def set_output(self, iEnable, iSetDirOut, iSetDataOut):
        self.bulk_write(
            [CH341A.PORT.SET_OUTPUT, 0x6A, iEnable & 0x1F,
             iSetDataOut >> 8 & 0xEF,
             iSetDirOut >> 8 & 0xEF | 0x10,
             iSetDataOut & 0xFF,
             iSetDirOut & 0xFF,
             iSetDataOut >> 16 & 0x0F, 0, 0, 0])


    def set_output2(self, output_pins = [], high_pins = [],
                    d15_d8_data_enable = True, d15_d8_dirc_enable = True,
                    d7_d0_data_enable = True, d7_d0_dirc_enable = True, d23_d16_data_enable = True):

        iEnable = int(d15_d8_data_enable) << 0 | \
                  int(d15_d8_dirc_enable) << 1 | \
                  int(d7_d0_data_enable) << 2 | \
                  int(d7_d0_dirc_enable) << 3 | \
                  int(d23_d16_data_enable) << 4

        bits_map = dict((('D0', 0), ('D1', 1), ('D2', 2), ('D3', 3), ('D4', 4), ('D5', 5), ('D6', 6), ('D7', 7),
                         ('ERR', 8), ('PEMP', 9), ('INT', 10), ('SLCT', 11), ('WAIT', 13), ('DATAS', 14), ('ADDRS', 15),
                         ('RESET', 16), ('WRITE', 17), ('SCL', 18), ('SDA', 29)))

        directions = 0
        for pin in output_pins:
            directions = directions | (1 << bits_map[pin])

        outputs = 0
        for pin in high_pins:
            outputs = outputs | (1 << bits_map[pin])

        self.set_output(iEnable, directions, outputs)


    @property
    def i2c(self):
        from .adapters.micropython import machine
        from .controllers.i2c import I2cController

        ctrl = I2cController(device = self)
        return machine.I2C(controller = ctrl)


    @property
    def gpio(self):
        from .controllers.gpio import GpioPort

        return GpioPort(device = self)


    @property
    def GPIO(self):
        return self.gpio
