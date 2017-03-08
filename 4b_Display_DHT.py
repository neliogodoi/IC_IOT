# Easy code for selection AP or STA mode on ESP8266
import machine
import ssd1306
import time
import dht

DHT = dht.DHT22(machine.Pin(2))
i2c = machine.I2C(sda=machine.Pin(4), scl=machine.Pin(5))
display = ssd1306.SSD1306_I2C(64, 48, i2c)

while True:
    time.sleep(2)
    DHT.measure()
    t = str(int(DHT.temperature()))+" C"
    h = str(int(DHT.humidity()))+" %"
    print(t," ",h)
    display.fill(0)
    display.text(t,2,10)
    display.text(h,2,30)
    display.show()