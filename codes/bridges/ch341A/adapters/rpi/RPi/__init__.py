from bridges.ch341A import CH341A

from .. import gpio


GPIO = gpio.GPIO(device = CH341A())
