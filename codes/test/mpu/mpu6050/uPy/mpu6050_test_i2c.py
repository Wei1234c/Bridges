from bridges.ftdi.controllers.i2c import I2cController

from test.mpu.mpu6050.uPy.mpu6050 import accel


# from machine import I2C, Pin
# i2c = I2C(scl=Pin(5), sda=Pin(4))


i2c = I2cController().I2C()

accelerometer = accel(i2c)
values = accelerometer.get_values()
print(values)
