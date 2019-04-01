from bridges.ch341A import CH341A


ctrl = CH341A().gpio

print(ctrl.addressable_pins)
import bridges.interfaces.micropython.machine as I_machine


pin_in = ctrl.Pin('D5', mode = I_machine.Pin.IN)
pin_out = ctrl.Pin('D6', mode = I_machine.Pin.OUT)

print(ctrl.pins_values)
print(ctrl.pins_values_list)

print('pin_in:', pin_in())



def blinks(pin):
    from time import sleep

    def blink(delay = 0.2):
        pin.toggle()
        sleep(delay)
        pin.toggle()
        sleep(delay)


    for i in range(5):
        print(i)
        blink()



blinks(pin_out)

ctrl.terminate()
