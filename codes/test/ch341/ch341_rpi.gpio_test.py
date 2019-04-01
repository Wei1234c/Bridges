from bridges.ch341A.adapters.rpi.RPi import GPIO


GPIO.setmode(GPIO.BOARD)
GPIO.setmode(GPIO.BCM)

mode = GPIO.getmode()

channel = 6
GPIO.setup(channel, GPIO.OUT, initial = GPIO.HIGH)



def blinks(pin):
    from time import sleep

    channel = pin
    GPIO.setup(channel, GPIO.OUT, initial = GPIO.HIGH)

    def blink(delay = 0.2):
        GPIO.output(channel, GPIO.HIGH)
        sleep(delay)
        GPIO.output(channel, GPIO.LOW)
        sleep(delay)


    for i in range(5):
        print(i)
        blink()

blinks(pin = 6)

GPIO.terminate()