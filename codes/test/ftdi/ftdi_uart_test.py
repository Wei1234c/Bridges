from bridges.ftdi.controllers.uart import UartController


ctrl = UartController()
# ctrl = UartController(product = 'ft2232h', interface = 2)
port = ctrl.Serial()
# port = ctrl.UART()
# port = ctrl.get_port()

# Send bytes
r = port.write(b'Hello World')
print(r)

# # Receive bytes
# data = port.read(1024)
