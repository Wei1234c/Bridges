from bridges.ftdi.controllers.i2c import I2cController
from display_ssd1306_i2c import Display


ctrl = I2cController()
# ctrl = I2cController(product = 'ft2232h', interface = 2)
i2c = ctrl.I2C(freq = 8e6)
# i2c = ctrl.get_i2c()
i2c.scan()

d = Display(i2c)
d.clear()
d.rect(0, 0, 30, 30, 56)
d.fill_rect(0, 0, 30, 30, 56)
d.hline(0, 0, 60, 56)
d.vline(0, 0, 60, 56)
d.line(0, 0, 60, 60, 56)
d.pixel(40, 40, 56)
d.show()

ctrl.terminate()