# Easy code for selection AP or STA mode on ESP8266
from machine import Pin
import time
import dht

DHT = dht.DHT22(Pin(2))

while True:
    time.sleep(2)
    DHT.measure()
    print("Temperatura: ",DHT.temperature(),"°C")
    print("Humidade:",DHT.humidity(),"%")