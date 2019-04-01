"""
It is not necessary to define this interface, since :

    pyftdi.serialext.protocol_ftdi.Serial
        inherits
    FtdiSerial
        inherits
    serial.serialutil.SerialBase

    so pyftdi.serialext.protocol_ftdi.Serial surely implements the interface.
"""

from serial.serialutil import SerialBase



class Serial(SerialBase):
    """Serial port implementation for .NET/Mono."""

    BAUDRATES = (50, 75, 110, 134, 150, 200, 300, 600, 1200, 1800, 2400, 4800,
                 9600, 19200, 38400, 57600, 115200)


    def open(self):
        """\
        Open port with current settings. This may throw a SerialException
        if the port cannot be opened.
        """
        raise NotImplementedError()


    def _reconfigure_port(self):
        """Set communication parameters on opened port."""
        raise NotImplementedError()


    def close(self):
        """Close port"""
        raise NotImplementedError()


    #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    @property
    def in_waiting(self):
        """Return the number of characters currently in the input buffer."""
        raise NotImplementedError()


    def read(self, size = 1):
        """\
        Read size bytes from the serial port. If a timeout is set it may
        return less characters as requested. With no timeout it will block
        until the requested number of bytes is read.
        """
        raise NotImplementedError()


    def write(self, data):
        """Output the given string over the serial port."""
        raise NotImplementedError()


    def reset_input_buffer(self):
        """Clear input buffer, discarding all that is in the buffer."""
        raise NotImplementedError()


    def reset_output_buffer(self):
        """\
        Clear output buffer, aborting the current output and
        discarding all that is in the buffer.
        """
        raise NotImplementedError()


    def _update_break_state(self):
        """
        Set break: Controls TXD. When active, to transmitting is possible.
        """
        raise NotImplementedError()


    def _update_rts_state(self):
        """Set terminal status line: Request To Send"""
        raise NotImplementedError()


    def _update_dtr_state(self):
        """Set terminal status line: Data Terminal Ready"""
        raise NotImplementedError()


    @property
    def cts(self):
        """Read terminal status line: Clear To Send"""
        raise NotImplementedError()


    @property
    def dsr(self):
        """Read terminal status line: Data Set Ready"""
        raise NotImplementedError()


    @property
    def ri(self):
        """Read terminal status line: Ring Indicator"""
        raise NotImplementedError()


    @property
    def cd(self):
        """Read terminal status line: Carrier Detect"""
        raise NotImplementedError()

    # - - platform specific - - - -
    # none
