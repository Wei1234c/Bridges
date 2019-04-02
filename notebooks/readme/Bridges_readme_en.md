
# Bridges 
### PC as an ESP32 simulator ?
### Pretend your PC a Raspberry Pi or an ESP32 to connect I2C/SPI/GPIO/UART peripherals. 


[GitHub repo.](https://github.com/Wei1234c/Bridges)

Wei Lin  
2019-4-2

![Grand Island bridges](https://raw.githubusercontent.com/Wei1234c/Bridges/master/jpgs/Between_the_Grand_Island_bridges.jpg)  

## [Usage scenarios]
Read on if these scenarios suit you:
- Use the PC to drive (via bus-converter) [I2C](https://en.wikipedia.org/wiki/I%C2%B2C) / [SPI](https://en.wikipedia.org/wiki/SPI) / [GPIO](https://en.wikipedia.org/wiki/General-purpose_input/output) / [UART](https://en.wikipedia.org/wiki/Universal_asynchronous_receiver-transmitter) interfaced peripheral devices.
     - For example, using SPI-interfaced [SX1278 LoRa transceiver](https://github.com/Wei1234c/SX127x_driver_for_MicroPython_on_ESP8266), [send and receive LoRa message packets](https://youtu.be/Ae9dvGm-bCQ) directly.
- On your PC, simulating the I2C / SPI / GPIO / UART intreface objects of ESP32 / Raspberry, in order to develop the peripheral device drivers in the [PyCharm](https://www.jetbrains.com/pycharm/) environment, you can [ set breakpoints and inspect variables easily](https://youtu.be/rhYNySJQ0Rg). 
     - No more "print" to debug, no more repeatedly uploading code to the controller.

## [Motivations]

- **Need to use some I2C/SPI/GPIO/UART interfaced device with my PC**:
    - One of my Python projects needs to use a SPI-interfaced device.
    - However, there is no external SPI interface available on the PC, therefore comes the bus-converter.
- **Bus-Converters selection**:
    - There are many USB to I2C/SPI/GPIO/UART converters available on the market.[FT232H (1 channel)](www.ftdichip.com/Products/ICs/FT232H.htm) / [FT2232H (2 channels)](https://www.ftdichip.com/Products/ICs/FT2232H.htm) from [FTDI]([https://www.ftdichip.com/) and [CH341](http://www.wch.cn/products/CH341.html) from [WCH](http://www.wch.cn/) ... is popular. FTDI's documentation and development resources are quite complete and relatively easy to develop.
    - [PyFtdi](http://eblot.github.io/pyftdi/) was choosen to drive FTDI chips, it only depands on [PyUSB](https://github.com/walac/pyusb/blob/master/docs/tutorial.rst). In addition, we nee also...
- **Drivers for the device**:
    - Besides communicating with devices via I2C/SPI/GPIO/UART, we also need drivers. We need [SSD1306 (Display Panel Control IC) driver](https://github.com/adafruit/Adafruit_SSD1306) to use the OLED display.
    - Many of those drivers can be found in [ESP8266](https://www.espressif.com/en/products/hardware/esp8266ex/overview) / [ESP32](https://www.espressif.com/En/products/hardware/esp32/overview) / [Raspberry Pi](https://www.raspberrypi.org/) communities. They are probably [written in (Mico) Python](https://github.com/lemariva/uPySensors), some can run directly on PC with little or no modification, it saves time to re-use them, but...
- **Requires Adapters to convert interfaces**:
    - These drivers were originally designed to go along with, for example, interface objects such as [machine.SPI](https://docs.micropython.org/en/latest/library/machine.SPI.html) or [spidev.SpiDev](https://github.com/doceme/py-spidev).
    - They have interfaces different from [SPI operation functions provided by PyFtdi](http://eblot.github.io/pyftdi/api/spi.html#pyftdi.spi.SpiPort),  we need **[Adapters](https://en.wikipedia.org/wiki/Adapter_pattern)** to glue them together.
- **Pretend your PC an ESP8266 / ESP32 / Raspberry Pi**:
    - As long as the device driver can run on a PC, and the SPI interface object it faces has exactly the same behavior of the SPI interface object on the ESP32, then the PC "IS" an ESP32 to the device driver. So in this cases, **PC is an ESP32 simulator**, at least to the device driver. So, we can...
- **Utilize powerful development resources and debugging environment from PC**:
    - For example, when developing a device driver, you can use [PyCharm](https://www.jetbrains.com/pycharm/) to set **breakpoints** and to **inspect variables** whenever needed.
    - No more "print" to debug, no more repeatedly uploading code to the controller. 


<table  align="center">
  <tr >
    <th>FT232H</th>
    <th>FT2232H</th>
    <th>CH341A</th> 
  </tr>
  <tr>
    <td><img src='https://raw.githubusercontent.com/Wei1234c/Bridges/master/jpgs/FT232H.jpg'  width="320"  ></td>
    <td><img src='https://raw.githubusercontent.com/Wei1234c/Bridges/master/jpgs/FT2232H.jpg'  width="320"  ></td>
    <td><img src='https://raw.githubusercontent.com/Wei1234c/Bridges/master/jpgs/CH341a.jpg'  width="320"  ></td> 
  </tr> 
</table>



## [Goals and Features]

- Writing a package to simulate the I2C/SPI/GPIO/UART interface objects for MicroPython+ESP8266/ESP32 and Raspberry Pi on PC:
   - Interface objects in MicroPython + ESP8266 / ESP32 environment:
       - machine.I2C
       - machine.SPI
       - machine.Pin
       - machine.UART -
   - Interface objects in the Raspberry Pi environment:
       - smbus2.SMbus
       - spidev.SpiDev
       - RPi.GPIO
       - PySerial.Serial
- Can drive many bus-converters simultaneously:
     - Multiple bus-converters can be connected at the same time, and the number is limited only by the specification of USB and power supply capability.
- Can function under Windows / Linux:
     - No modification is required.
- Can be used on PC / Raspberry Pi or any machines that can run PyFtdi package:
     - No modification is required.

## [How to use]
### Simulating for MicroPython + ESP8266 / ESP32
- **For [machine.I2C](https://docs.micropython.org/en/latest/library/machine.I2C.html)**

```
# On ESP32 with MicroPython
From machine import I2C

I2c = I2C(freq = 400000)
```
---

```
# On PC
From bridges.ftdi.controllers.i2c import I2cController
I2C = I2cController().I2C

I2c = I2C(freq = 400000)
```
---
    
- **For [machine.SPI](https://docs.micropython.org/en/latest/library/machine.SPI.html)**

```
# On ESP32 with MicroPython
From machine import SPI

Spi = SPI(id, baudrate = 10000000, polarity = 0, phase = 0)
Spi.init()
```
---
```
# On PC
From bridges.ftdi.controllers.spi import SpiController
SPI = SpiController().SPI

Spi = SPI(id, baudrate = 10000000, polarity = 0, phase = 0)
Spi.init()
```
  
  
- **For [machine.Pin](https://docs.micropython.org/en/latest/library/machine.Pin.html)**

```
# On ESP32 with MicroPython
From machine import Pin

P0 = Pin(0, Pin.OUT)
P0.value(0)
P0.value(1)

P2 = Pin(2, Pin.IN, Pin.PULL_UP)
Print(p2.value())
```
---

```
# On PC
From bridges.interfaces.micropython.machine import Pin
From bridges.ftdi.controllers.gpio import GpioController
Machine = GpioController()

P0 = machine.Pin(0, mode = Pin.OUT)
P0.value(0)
P0.value(1)

P2 = machine.Pin(2, mode = Pin.IN)
Print(p2.value())
```
  
- **For [machine.UART](https://docs.micropython.org/en/latest/library/machine.UART.html)**

```
# On ESP32 with MicroPython
From machine import UART

Uart = UART(1, 9600)
Uart.init(9600, bits=8, parity=None, stop=1)
```
---
```
# On PC
From bridges.ftdi.controllers.uart import UartController
UART = UartController().UART

Uart = UART(1, 9600)
Uart.init(9600, bits=8, parity=None, stop=1)
```

###  Simulating for Raspberry Pi 
- **For [smbus2.SMbus](https://pypi.org/project/smbus2/)**

```
# On Raspberry
from smbus2 import SMBus 

bus = SMBus(1)
b = bus.read_byte_data(80, 0)
print(b) 
```  
---
```
# On PC
from bridges.ftdi.controllers.i2c import I2cController
SMBus = I2cController().SMBus

bus = SMBus(1)  # the bus number actually doesn't matter.
b = bus.read_byte_data(80, 0)
print(b) 
```

- **For [spidev.SpiDev](https://pypi.org/project/spidev/)**

```
# On Raspberry
import spidev

spi = spidev.SpiDev()
spi.open(bus, device)
to_send = [0x01, 0x02, 0x03]
spi.xfer(to_send)
```  
---
```
# On PC
import controller
from bridges.ftdi.controllers.spi import SpiController
spidev = SpiController() 

spi = spidev.SpiDev()
spi.open(bus, device)
to_send = [0x01, 0x02, 0x03]
spi.xfer(to_send)

```

- **For [RPi.GPIO](https://sourceforge.net/p/raspberry-gpio-python/wiki/Examples/)**

```
# On Raspberry
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD) 
GPIO.setup(6, GPIO.OUT)
```  
---
```
# On PC
from bridges.ftdi.adapters.rpi.RPi import GPIO 

GPIO.setmode(GPIO.BOARD)  # mode actuall doesn't  matter.
GPIO.setup(6, GPIO.OUT)

```
- **For [pySerial.Serial](https://pyserial.readthedocs.io/en/latest/shortintro.html)**

```
# On Raspberry
import serial
ser = serial.Serial('/dev/ttyUSB0') 

print(ser.name)        
ser.write(b'hello')     
ser.close()            
```  
---
```
# On PC
from bridges.ftdi.controllers.uart import UartController
ser = UartController().Serial() 

print(ser.name)        
ser.write(b'hello')     
ser.close()      
```

## [Test results]
- Breakpoints and variables inspection
[![Breakpoints and variables inspection](https://raw.githubusercontent.com/Wei1234c/Bridges/master/jpgs/Breakpoints_and_variables_inspection.gif)](https://youtu.be/rhYNySJQ0Rg)   


- Transceive LoRa packages directly from your laptop
[![Transceive LoRa packages directly from your laptop](https://raw.githubusercontent.com/Wei1234c/Bridges/master/jpgs/Transceive_LoRa_packages_from_laptop.gif)](https://youtu.be/Ae9dvGm-bCQ)   

#### Notes
- Mainly supports FTDI chips for now. 
    - For CH341A:
        - Only I2C and GPIO functions are implemented, no SPI
        - UART can be driven directly with the driver from WCH.
- FTDI chip limitations
     - No IRQ. 
         - The FT232H/FT2232H does not have endpoint of "interrupt input" type, IRQ functionality can only achieved with polling, which is too CPU intensive.
     - No PWM. PyFtdi, FT232H/FT2232H doesn't support.
     - In the same channel, the functionality of GPIO can coexist with SPI, but not with I2C/UART.
     - GPIO has no pull-up / pull-down functions.

#### [References](https://github.com/Wei1234c/Bridges/tree/master/references)

