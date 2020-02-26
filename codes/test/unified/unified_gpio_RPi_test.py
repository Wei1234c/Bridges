import RPi.GPIO as GPIO
from bridges.tools import unified


GPIO.setmode(GPIO.BCM)

try:
    GPIO.cleanup()
except Exception as e:
    print(e)



pin_id = 47
pin_unified = unified.Pin.from_RPi(GPIO, pin_id, is_output = True)
pin_unified.high()
