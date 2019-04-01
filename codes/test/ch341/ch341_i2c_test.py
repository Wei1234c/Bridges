from bridges.ch341A import CH341A


ch341A = CH341A()
# ch341A.set_i2c_speed(4e2)
# ch341A.set_stream(0x00)
# ch341A.clear_buffers()
# print(ch341A.endpoints[0x82].direction)
# print(ch341A)

# mask = 0x3F
# ch341.set_D5_D0(iSetDirOut = mask, iSetDataOut = mask)
# print(ch341.get_pin_status('D5'))

# ch341A.set_output2(output_pins = ['D5'], high_pins = ['D5'])
# # ch341A.set_output2(output_pins = ['D7'], high_pins = ['D7'])
# print(ch341A.status)

i2c = ch341A.i2c
# smbus2 = ch341A.smbus2
# i2c.scan_i2c_bus()
i2c.scan()
# ch341A.reset()
# cfg = ch341A.get_active_configuration()
# print(cfg.bConfigurationValue)

# desc = ch341A.control_read(bRequest = 0x06, wValue = 0x0100, wIndex = 0, wLength = 18, type = usb.util.CTRL_TYPE_STANDARD)
# print( desc)
# print(len(desc))

# for i in range(0xff):
#     try:
#         desc = ch341A.control_read(bRequest = i, wValue = 0, wIndex = 0, wLength = 1024,
#                                   type = usb.util.CTRL_TYPE_STANDARD)
#         print(hex(i), desc)
#     except:
#         pass

# from bridges.smbus2 import SMBus
#
# # Open i2c bus 1 and read one byte from address 80, offset 0
# bus = SMBus(1)
# b = bus.read_byte_data(80, 0)
# print(b)
# bus.close()

# from bridges.ch341A import *
# from display_ssd1306_i2c import Display
# i2c = I2C()
# oled = Display(i2c)
# text = 't'
# oled.show_text( text, x = 0, y = 0, clear_first = True, show_now = True, hold_seconds = 0)


# ch341A.set_output2()

from adafruit import Display


d = Display(i2c)  # d = Display(smbus2)
d.rect(0, 0, 30, 30, 56)
d.fill_rect(0, 0, 30, 30, 56)
d.hline(0, 0, 60, 56)
d.vline(0, 0, 60, 56)
d.line(0, 0, 60, 60, 56)
d.pixel(40, 40, 56)
d.show()

ch341A.close()
