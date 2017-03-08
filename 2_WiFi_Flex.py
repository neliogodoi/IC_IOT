# Easy code for AP or STA selection mode on ESP8266 by flag
from machine import Pin
import network
import socket
import time
import ure
# select WiFi mode: 0 = AP | 1 = STA
MODE = 0 
ssid = "ESP"
password = "12345678"
# settings default for wifi
ap = network.WLAN(network.AP_IF)
sta = network.WLAN(network.STA_IF)
sta.active(False)
ap.active(True)
ap.config(essid='ESP', password='12345678')
print(ap.ifconfig())
# Setting LED of device
light = Pin(2, Pin.OUT)
light.value(1) # off LED of device
# Setting socket for listening clients
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)
print('listening on', addr)

if (MODE == 0):
    ap.config(essid=ssid,password=password)
    print(ap.ifconfig())
else:
    ap.active(False)
    sta = network.WLAN(network.STA_IF)
    sta.active(True)
    sta.connect(ssid, password)
    time.sleep(10)
    print(sta.ifconfig())

html = """<!DOCTYPE html><html><head><title>Interruptor Wi-Fi</title><style type="text/css">body{ background-color: #fc0;} #Lampada{ margin: 2px solid ; height: 30px; position: absolute; left: 30%;}</style></head><body><script type="text/javascript">function request(url) {var xhttp;if (window.XMLHttpRequest) {xhttp = new XMLHttpRequest();} else {xhttp = new ActiveXObject("Microsoft.XMLHTTP");}xhttp.onreadystatechange = function() {if (this.readyState == 4 && this.status == 200) {alert('Finished');}};xhttp.open("GET", url, true);xhttp.send();}</script><div id="Lampada"></h1><button type="submit" onclick="request('LightStatus=On');">Ligar</button><button type="submit" onclick="request('LightStatus=Off');">Desligar</button> </div></body></html>"""

while True:
    cl, addr = s.accept()
    print('client connected from', addr)
    cl_file = cl.makefile('rwb', 0)
    while True:
        line = cl_file.readline()
        strLine = str(line)
        if not line or line == b'\r\n':
            cl.send(html)
            break
        if not ure.search('LightStatus=', strLine):
            continue
        else:
            status = strLine.split(' ')[1].split('=')[1]
            cl.send(html)
            if status == 'On':
                light.value(1)
            else:
                light.value(0)
        break
    cl.close()