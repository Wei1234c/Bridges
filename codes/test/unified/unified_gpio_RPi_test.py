import RPi.GPIO as GPIO
from bridges.tools import unified
import time


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

try:
    GPIO.cleanup()
except Exception as e:
    print(e)

pin_id = 47
pin_unified = unified.Pin.from_RPi(GPIO, pin_id, is_output = True)



def blink(times = 1):
    for i in range(times):
        pin_unified.high()
        time.sleep(0.5)
        pin_unified.low()
        time.sleep(0.5)



blink(3)
