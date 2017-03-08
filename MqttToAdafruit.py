import network
import time
import machine
import bme280 # INSERIDO
import gc
from simple import MQTTClient

i2c = machine.I2C(sda=machine.Pin(4), scl=machine.Pin(5))
bme = bme280.BME280(i2c=i2c)

WifiSSID = "Fisica"
WifiPSWD = "Fisic@42"
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.connect(WifiSSID, WifiPSWD)
time.sleep(5)
while not sta.isconnected():
  print(".")
print(sta.ifconfig())
  
# connect ESP8266 to Adafruit IO using MQTT
myMqttClient = "neliogodoi-mqtt-client"
server = "io.adafruit.com" 
username = "neliogodoi" 
adafruitAioKey = "92caff99dd304298b13110e28e18f540"
c = MQTTClient(myMqttClient, server, 0, username, adafruitAioKey)
c.connect()
print("connected")

while True:
  temperature = bme.values[0]
  pressure = bme.values[1]
  humidity = bme.values[2]
  c.publish("neliogodoi/feeds/feed-Temp", str(temperature))  # publish temperature
  c.publish("neliogodoi/feeds/feed-Pres", str(pressure))     # publish pressure
  c.publish("neliogodoi/feeds/feed-Humi", str(humidity))     # publish humity
  print("Published")
  time.sleep(5)

c.disconnect() 
