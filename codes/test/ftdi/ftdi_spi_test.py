import bridges.interfaces.micropython.machine as machine

from bridges.ftdi.controllers.spi import SpiController

from display_ssd1306_spi import Display


ctrl = SpiController()
# ctrl = SpiController(product = 'ft2232h', interface = 2)
spi = ctrl.get_spi(cs = 0, freq = 12E6, mode = 0)
# spi = ctrl.SPI()
gpio = ctrl.get_gpio()

pin_in = gpio.Pin('ADBUS5', mode = machine.Pin.IN)
pin_out = gpio.Pin('ADBUS6', mode = machine.Pin.OUT, value = 1)
# pin_in = gpio.Pin('BDBUS5', mode = machine.Pin.IN)
# pin_out = gpio.Pin('BDBUS6', mode = machine.Pin.OUT, value = 1)

print(gpio.pins_values)
print(gpio.pins_values_list)



def blinks():
    from time import sleep

    def blink(delay = 0.2):
        pin_out.toggle()
        sleep(delay)
        pin_out.toggle()
        sleep(delay)


    for i in range(3):
        print(i)
        blink()



# blinks()

dc = gpio.Pin('ADBUS4', mode = machine.Pin.OUT)
res = gpio.Pin('ADBUS5', mode = machine.Pin.OUT)
cs = gpio.Pin('ADBUS6', mode = machine.Pin.OUT)

# dc = gpio.Pin('BDBUS4', mode = machine.Pin.OUT)
# res = gpio.Pin('BDBUS5', mode = machine.Pin.OUT)
# cs = gpio.Pin('BDBUS6', mode = machine.Pin.OUT)

d = Display(spi, dc, res, cs)
d.clear()
d.rect(0, 0, 30, 30, 56)
d.fill_rect(0, 0, 30, 30, 56)
d.hline(0, 0, 60, 56)
d.vline(0, 0, 60, 56)
d.line(0, 0, 60, 60, 56)
d.pixel(40, 40, 56)
d.show()

ctrl.terminate()
