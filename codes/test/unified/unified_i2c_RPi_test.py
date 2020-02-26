from smbus2 import SMBus
from bridges.tools import unified

bus = SMBus(1)
b = bus.read_byte_data(80, 0)
print(b)

i2c = unified.I2C.from_RPi(bus)

i2c.readfrom(0x30, 1)
