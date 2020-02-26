import machine
import unified
# from bridges.tools import unified

pin_id = 2
pin = machine.Pin(pin_id, machine.Pin.OUT)

pin_unified = unified.Pin.from_uPy(pin)

pin_unified.high()
