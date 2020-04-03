import RPi.GPIO as GPIO
import spidev

from bridges.tools import unified


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

try:
    GPIO.cleanup()
except Exception as e:
    print(e)



def get_spi():
    spi = None

    try:
        spi = spidev.SpiDev()
        bus = 0
        device = 0
        spi.open(bus, device)
        spi.max_speed_hz = 10000000
        spi.mode = 0b00
        spi.lsbfirst = False

    except Exception as e:
        print(e)
        GPIO.cleanup()
        if spi:
            spi.close()
            spi = None

    return spi



pin_id = 47
# pin_id = None
spi = unified.SPI.from_RPi(get_spi(), GPIO = GPIO, pin_ss_id = pin_id)
# spi = unified.SPI.from_RPi(get_spi())

result = spi.transfer(address = 3, value = 0x00)
print(result)
