from bridges.interfaces import *



class Serial(I_serial.Serial):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
