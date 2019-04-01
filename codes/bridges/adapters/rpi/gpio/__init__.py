from bridges.interfaces import *



class PWM:

    def __init__(self, channel, frequency):
        self.channel = channel
        self.frequency = frequency
        self.duty_cycle = 50


    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()


    def start(self, duty_cycle):
        raise NotImplementedError()


    def ChangeFrequency(self, frequency):
        raise NotImplementedError()


    def ChangeDutyCycle(self, duty_cycle):
        raise NotImplementedError()


    def stop(self):
        raise NotImplementedError()



class GPIO(I_gpio.GPIO):
    VERSION = 0.1

    BOARD = 10
    BCM = 11

    IN = 1
    OUT = 0

    PUD_UP = 22
    PUD_DOWN = 21

    HIGH = 1
    LOW = 0

    RISING = 31
    FALLING = 32
    BOTH = 33


    def __exit__(self):
        raise NotImplementedError()


    def __del__(self):
        raise NotImplementedError()


    def PWM(self, channel, frequency):
        return PWM(channel, frequency)


    @property
    def RPI_INFO(self):
        import platform

        info = platform.platform()
        return dict(PLATFORM = info, P1_REVISION = info)


    def setmode(self, mode):
        self._mode = mode


    def getmode(self):
        return self._mode


    def gpio_function(self, channel):
        direction = self.get_pin_direction(channel)
        return ['OUT' if direction else 'IN']


    def setwarnings(self, warnnin = True):
        raise NotImplementedError()


    def input(self, channel):
        return self.get_pin_value(channel)


    def output(self, channel, state):
        if hasattr(channel, '__len__'):
            if hasattr(state, '__len__'):
                for ch, st in zip(channel, state):
                    self.output(ch, st)
            else:
                for ch in channel:
                    self.output(ch, state)
        else:
            self.set_pin_value(channel, state)


    def wait_for_edge(self, channel, mode, timeout = None):
        raise NotImplementedError()


    def add_event_detect(self, channel, mode, callback = None, bouncetime = None):
        raise NotImplementedError()


    def event_detected(self, channel):
        raise NotImplementedError()


    def add_event_callback(self, channel, callback, bouncetime = None):
        raise NotImplementedError()


    def remove_event_detect(self, channel):
        raise NotImplementedError()


    def cleanup(self, channel = None):
        self.terminate()
