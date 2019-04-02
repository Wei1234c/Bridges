# https://sourceforge.net/p/raspberry-gpio-python/wiki/Examples/


class GPIO:
    BOARD = 10
    BCM = 11
    BOTH = 33
    IN = 1
    OUT = 0
    LOW = 0
    HIGH = 1
    PUD_UP = 22
    PUD_DOWN = 21
    RPI_INFO = {}
    RISING = 31
    FALLING = 32
    VERSION = '???'


    def setmode(self, mode):
        raise NotImplementedError()


    def getmode(self):
        raise NotImplementedError()


    def setwarnings(self, value = False):
        raise NotImplementedError()


    def setup(self, channels, mode = IN, pull_up_down = None, initial = None):
        raise NotImplementedError()


    def input(self, channels):
        raise NotImplementedError()


    def output(self, channels, states):
        raise NotImplementedError()


    def cleanup(self, channels = None):
        raise NotImplementedError()


    def wait_for_edge(self, channel, RISING):
        raise NotImplementedError()


    def add_event_detect(self, channel, edge = RISING):
        raise NotImplementedError()


    def event_detected(self, channel):
        raise NotImplementedError()


    def add_event_callback(self, channel, callback = None, bouncetime = None):
        raise NotImplementedError()


    def remove_event_detect(self, channel):
        raise NotImplementedError()


    class PWM:

        def __init__(self, channel, frequency):
            raise NotImplementedError()


        def start(self, dc):
            raise NotImplementedError()


        def ChangeFrequency(self, freq):
            raise NotImplementedError()


        def ChangeDutyCycle(self, dc):
            raise NotImplementedError()


        def stop(self):
            raise NotImplementedError()
