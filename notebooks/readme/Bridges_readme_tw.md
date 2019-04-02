
# Bridges 
### PC as an ESP32 simulator ?
### Pretend your PC a Raspberry Pi or an ESP32 to connect I2C/SPI/GPIO/UART peripherals. 


[GitHub repo.](https://github.com/Wei1234c/Bridges)

Wei Lin  
2019-4-2

![Grand Island bridges](https://raw.githubusercontent.com/Wei1234c/Bridges/master/jpgs/Between_the_Grand_Island_bridges.jpg)  

## [使用情境]
先說說 使用情境，合用的話再往下看:  
- 使用 PC 直接驅動  [I2C](https://en.wikipedia.org/wiki/I%C2%B2C) / [SPI](https://en.wikipedia.org/wiki/SPI) / [GPIO](https://en.wikipedia.org/wiki/General-purpose_input/output) / [UART](https://en.wikipedia.org/wiki/Universal_asynchronous_receiver-transmitter) 周邊裝置
    - 例如 控制 SPI介面的 [SX1278 LoRa transceiver](https://github.com/Wei1234c/SX127x_driver_for_MicroPython_on_ESP8266), [直接收發 LoRa 訊息封包](https://youtu.be/Ae9dvGm-bCQ)。    
- 在 [PyCharm](https://www.jetbrains.com/pycharm/) 的環境下開發 I2C/SPI/GPIO/UART裝置 的 驅動程式，可以 [設定中斷點 並隨時 檢視變數值](https://youtu.be/rhYNySJQ0Rg)。
    - 不需要插入許多 print 指令，也不需要重複地 上傳程式碼到 控制器 上。

## [緣由] 

- **需要使用PC 直接連接 I2C/SPI/GPIO/UART介面的周邊裝置**:
    - 最初是因為手上的一個 Python 專案，必須連接上某個 SPI 介面的裝置抓取資料來計算。
    - PC環境下的 運算能量，與強大的 Python套件資源，可以做到一些在 MicroPython + ESP32 甚至 Raspberry Pi 上無法做到的事情。
    - 但是因為 PC 上並沒有 外接的SPI介面 可供連接，必須透過轉換器。
- **轉換器 的選擇**:
    - 市面上有很多種 USB to I2C/SPI/GPIO/UART 的轉換器，常見的有 [FTDI](https://www.ftdichip.com/) 的 [FT232H (1 channel)](https://www.ftdichip.com/Products/ICs/FT232H.htm) / [FT2232H (2 channels)](https://www.ftdichip.com/Products/ICs/FT2232H.htm) 和 [WCH](http://www.wch.cn/) 的 [CH341](http://www.wch.cn/products/CH341.html)...等數種。 FTDI 的文件與開發資源相當齊全，開發上相對容易一些。 
    - 已經有很多 libraries/套件 可以用來驅動 FTDI 的晶片，但考慮跨平台的可攜性，最後選擇使用 [PyFtdi](http://eblot.github.io/pyftdi/)，它透過 [PyUSB](https://github.com/walac/pyusb/blob/master/docs/tutorial.rst) 下達指令給 FTDI 晶片，相依的中間曾套件比較少一點。另外我們還...
- **需要 裝置的驅動程式**:        
    - 可以透過 FT232H/FT2232H，與 I2C/SPI/GPIO/UART 的週邊裝置溝通，但是另外還需要 裝置專屬的驅動程式。例如要驅動 OLED display，就需要 [SSD1306 (顯示面板控制 IC)的驅動程式](https://github.com/adafruit/Adafruit_SSD1306)。
    - 這些針對性的驅動程式 普遍地存在於  [ESP8266](https://www.espressif.com/en/products/hardware/esp8266ex/overview) / [ESP32](https://www.espressif.com/en/products/hardware/esp32/overview) / [Raspberry Pi](https://www.raspberrypi.org/) 的生態圈中，許多是[使用 (Mico)Python 撰寫的](https://github.com/lemariva/uPySensors)，有些不須修改，或者經過少許修改，就可以直接在 PC 上執行，因此可能可以重複利用，不須重新開發，但是...
- **需要 Adapters 來轉換介面**:
    - 這些驅動程式 原本是對接例如 [machine.SPI](https://docs.micropython.org/en/latest/library/machine.SPI.html) 或 [spidev.SpiDev](https://github.com/doceme/py-spidev) 之類的介面物件，與 [PyFtdi 所提供的 SPI操作函數](http://eblot.github.io/pyftdi/api/spi.html#pyftdi.spi.SpiPort) 有不少功能與定義上的差異，因此需要製作一層 **[Adapters](https://en.wikipedia.org/wiki/Adapter_pattern)**， 以便讓 這些驅動程式 能和 PyFtdi 無縫接軌，驅動周邊裝置。
- **將 PC 視同是 ESP8266 / ESP32 / Raspberry Pi **:
    - 如果裝置的驅動程式可以在PC上執行，而它所面對的 SPI介面物件，行為上和 ESP32上的SPI介面物件 一模一樣，那麼對 裝置的驅動程式 而言，PC就視同是一片 ESP32，因此在特定情況下，**PC就等同是一個 ESP32 的模擬器**，這樣我們就可以...
- **運用PC上強大的開發資源與除錯環境**:
    - 例如在開發裝置驅動程式的時候，就可以用例如 [PyCharm](https://www.jetbrains.com/pycharm/) 之類強大的 IDE，可以設定**中斷點**，並隨時**監看變數值**，應該會相當方便。
    - 不需要插入許多 print 指令，也不需要重複地 上傳程式碼到 控制器 上，程式整潔並節省開發時間。


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



## [目標]

- 寫一套 package，要能在PC上 模擬 MicroPython+ESP8266/ESP32 和 Raspberry Pi 上的 buses 功能界面： 
  - 模擬 MicroPython + ESP8266 / ESP32 環境下的:
      - machine.I2C
      - machine.SPI
      - machine.Pin
      - machine.UART              - 
  - 模擬 Raspberry Pi 環境下的:
      - smbus2.SMbus
      - spidev.SpiDev
      - RPi.GPIO
      - PySerial.Serial
- 要能搭配各種轉接器
    - 可同時連接多個轉換器，可擴增的 buses 數量只受到 USB bus 裝置數量上限 與 供電能力上 的限制。
- 要能在 Windows / Linux 下通用 
    - 同一套程式通用，不須做任何修改。
- 可以在 PC / Raspberry Pi 或其他可以使用 PyFtdi 套件的機器上通用
    - 同一套程式通用，不須做任何修改。

## [使用方式] 
### 模擬 MicroPython + ESP8266 / ESP32 上的介面
- **模擬 [machine.I2C](https://docs.micropython.org/en/latest/library/machine.I2C.html)**

```
# 在 MicroPython 的環境下
from machine import I2C

i2c = I2C(freq = 400000) 
```
---

```
# 在 PC 的環境下
from bridges.ftdi.controllers.i2c import I2cController
I2C = I2cController().I2C

i2c = I2C(freq = 400000)
```
--- 
    
- **模擬 [machine.SPI](https://docs.micropython.org/en/latest/library/machine.SPI.html)**

```
# 在 MicroPython 的環境下
from machine import SPI

spi = SPI(id, baudrate = 10000000, polarity = 0, phase = 0)
spi.init()
```
---
```
# 在 PC 的環境下
from bridges.ftdi.controllers.spi import SpiController 
SPI = SpiController().SPI

spi = SPI(id, baudrate = 10000000, polarity = 0, phase = 0) 
spi.init()
```
  
  
- **模擬 [machine.Pin](https://docs.micropython.org/en/latest/library/machine.Pin.html)**

```
# 在 MicroPython 的環境下
from machine import Pin 

p0 = Pin(0, Pin.OUT) 
p0.value(0)
p0.value(1)

p2 = Pin(2, Pin.IN, Pin.PULL_UP)
print(p2.value())
```
---

```
# 在 PC 的環境下
from bridges.interfaces.micropython.machine import Pin
from bridges.ftdi.controllers.gpio import GpioController 
machine = GpioController()  

p0 = machine.Pin(0, mode = Pin.OUT)
p0.value(0)
p0.value(1)

p2 = machine.Pin(2, mode = Pin.IN)
print(p2.value())
```
  
- **模擬 [machine.UART](https://docs.micropython.org/en/latest/library/machine.UART.html)**

```
# 在 MicroPython 的環境下
from machine import UART

uart = UART(1, 9600) 
uart.init(9600, bits=8, parity=None, stop=1)
```  
---
```
# 在 PC 的環境下
from bridges.ftdi.controllers.uart import UartController
UART = UartController().UART

uart = UART(1, 9600)
uart.init(9600, bits=8, parity=None, stop=1)
```

###  Raspberry Pi
- **模擬 [smbus2.SMbus](https://pypi.org/project/smbus2/)**

```
# 在 Raspberry Pi 的環境下
from smbus2 import SMBus 

bus = SMBus(1)
b = bus.read_byte_data(80, 0)
print(b) 
```  
---
```
# 在 PC 的環境下
from bridges.ftdi.controllers.i2c import I2cController
SMBus = I2cController().SMBus

bus = SMBus(1)  # the bus number actually doesn't matter.
b = bus.read_byte_data(80, 0)
print(b) 
```

- **模擬 [spidev.SpiDev](https://pypi.org/project/spidev/)**

```
# 在 Raspberry Pi 的環境下
import spidev

spi = spidev.SpiDev()
spi.open(bus, device)
to_send = [0x01, 0x02, 0x03]
spi.xfer(to_send)
```  
---
```
# 在 PC 的環境下
import controller
from bridges.ftdi.controllers.spi import SpiController
spidev = SpiController() 

spi = spidev.SpiDev()
spi.open(bus, device)
to_send = [0x01, 0x02, 0x03]
spi.xfer(to_send)

```

- **模擬 [RPi.GPIO](https://sourceforge.net/p/raspberry-gpio-python/wiki/Examples/)**

```
# 在 Raspberry Pi 的環境下
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD) 
GPIO.setup(6, GPIO.OUT)
```  
---
```
# 在 PC 的環境下
from bridges.ftdi.adapters.rpi.RPi import GPIO 

GPIO.setmode(GPIO.BOARD)  # mode actuall doesn't  matter.
GPIO.setup(6, GPIO.OUT)

```
- **模擬 [pySerial.Serial](https://pyserial.readthedocs.io/en/latest/shortintro.html)**

```
# 在 Raspberry Pi 的環境下
import serial
ser = serial.Serial('/dev/ttyUSB0') 

print(ser.name)        
ser.write(b'hello')     
ser.close()            
```  
---
```
# 在 PC 的環境下
from bridges.ftdi.controllers.uart import UartController
ser = UartController().Serial() 

print(ser.name)        
ser.write(b'hello')     
ser.close()      
```

## [測試實例]
- Breakpoints and variables inspection
[![Breakpoints and variables inspection](https://raw.githubusercontent.com/Wei1234c/Bridges/master/jpgs/Breakpoints_and_variables_inspection.gif)](https://youtu.be/rhYNySJQ0Rg)   


- Transceive LoRa packages directly from your laptop
[![Transceive LoRa packages directly from your laptop](https://raw.githubusercontent.com/Wei1234c/Bridges/master/jpgs/Transceive_LoRa_packages_from_laptop.gif)](https://youtu.be/Ae9dvGm-bCQ)   

#### Notes
- 目前主要支援 FTDI 晶片。CH341 下只有 I2C 和 GPIO 功能，無 SPI，但 UART 可直接透過 原廠的 driver 驅動
- FTDI 晶片的限制
    - 無 IRQ。因為 FT232H/FT2232H 並沒有 "interrupt input" 類型的 endpoint，要模擬 IRQ 的功能只能用 polling 的方式，太耗費 CPU 資源。
    - 無 PWM。PyFtdi、FT232H/FT2232H 並沒有支援。
    - 同一個 channel中，GPIO 的功能無法和 I2C/UART 共存，但是可以和 SPI共存。
    - GPIO 無 pull-up / pull-down 功能

#### [References](https://github.com/Wei1234c/Bridges/tree/master/references)

