import machine
import unified

# from bridges.tools import unified

scl_pin_id = 5
sda_pin_id = 4
freq = 400000
i2c = machine.I2C(scl = machine.Pin(scl_pin_id, machine.Pin.OUT),
                  sda = machine.Pin(sda_pin_id),
                  freq = freq)

i2c = unified.I2C.from_uPy(i2c)

i2c.readfrom(0x30, 1)
