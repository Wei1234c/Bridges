import controller
from bridges.ftdi.controllers.spi import SpiController


ctrl = SpiController()
SpiDev = ctrl.SpiDev()
GPIO = ctrl.GPIO()



class Controller(controller.Controller):
    # BOARD config
    ON_BOARD_LED_PIN_NO = 6  # RPi's on-board LED
    ON_BOARD_LED_HIGH_IS_ON = True
    GPIO_PINS = (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27,)

    # LoRa config
    PIN_ID_FOR_LORA_RESET = 5

    PIN_ID_FOR_LORA_SS = 7
    # PIN_ID_SCK = 11
    # PIN_ID_MOSI = 10
    # PIN_ID_MISO = 9

    PIN_ID_FOR_LORA_DIO0 = None
    PIN_ID_FOR_LORA_DIO1 = None
    PIN_ID_FOR_LORA_DIO2 = None
    PIN_ID_FOR_LORA_DIO3 = None
    PIN_ID_FOR_LORA_DIO4 = None
    PIN_ID_FOR_LORA_DIO5 = None


    def __init__(self,
                 pin_id_led = ON_BOARD_LED_PIN_NO,
                 on_board_led_high_is_on = ON_BOARD_LED_HIGH_IS_ON,
                 pin_id_reset = PIN_ID_FOR_LORA_RESET,
                 blink_on_start = (2, 0.5, 0.5)):

        self.spi = SpiDev
        super().__init__(pin_id_led,
                         on_board_led_high_is_on,
                         pin_id_reset,
                         blink_on_start)


    def prepare_pin(self, pin_id, in_out = GPIO.OUT):
        if pin_id is not None:
            return GPIO.setup(pin_id, in_out, initial = GPIO.HIGH)


    def prepare_irq_pin(self, pin_id):
        pin = self.prepare_pin(pin_id, GPIO.IN)
        if pin:
            pin.set_handler_for_irq_on_rising_edge = \
                lambda handler: GPIO.add_event_detect(pin._id,
                                                      GPIO.RISING,
                                                      callback = handler)
            pin.detach_irq = lambda: GPIO.remove_event_detect(pin._id)
            return pin


    def get_spi(self):
        return self.spi


    def prepare_spi(self, spi):
        return self.get_spi()


    def __exit__(self):
        GPIO.cleanup()
        self.spi.close()
