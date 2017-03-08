# Easy code for AP or STA selection mode on ESP8266 by WebServer
from machine import Pin
import network
import socket
import time
import ure

ap = network.WLAN(network.AP_IF)
sta = network.WLAN(network.STA_IF)
sta.active(False)
ap.active(True)
ap.config(essid='ESP', password='12345678') # Padrao

print(ap.ifconfig())
light = Pin(2, Pin.OUT) # LED test
light.value(1) # Desliga o LED da placa
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)
print('listening on', addr)

page = """<html><head><meta charset="UTF-8"/><title>Select Connection Mode Device</title></head><body><script type="text/javascript">function request() {var selection;var els = document.getElementsByName('selection');for (var i = 0; i < els.length; i++){if ( els[i].checked ) {selection = els[i].value;}}var ssid = document.getElementById('ssid').value;var passwd = document.getElementById('pass').value;var url = 'select/'+selection+'/'+ssid+'/'+passwd+'/';var xhttp;if (window.XMLHttpRequest) { xhttp = new XMLHttpRequest();} else { xhttp = new ActiveXObject("Microsoft.XMLHTTP");}xhttp.onreadystatechange = function() {if (this.readyState == 4 && this.status == 200) {alert('Finished!');}};;xhttp.open("POST", url, true);xhttp.send();}</script><div><input type="radio" name="selection" value="AP">AP</input><input type="radio" name="selection" value="STA">STA</input><p>SSID<br><input type="text" id='ssid'></input></p><p>PASS<br><input type="password" id='pass'></input></p><p><button onclick="request();">Enviar</button></p></div></body></html>"""
flag = 0
while(flag == 0):
    c, addr = s.accept()
    print('client connected from', addr)
    c_file = c.makefile('rwb', 0)
    while True:
        line = c_file.readline()
        strL = str(line)
        if not line or line == b'\r\n':
            c.send(page)
            break
        if not ure.search('select', strL):
            continue
        else:
            selection = strL.split('/')[2]
            ssid = strL.split('/')[3]
            password = strL.split('/')[4]
            c.send(page)
            flag = 1
            if (selection == 'AP'):
                ap.config(essid=ssid,password=password)
                print(ap.ifconfig())
            else:
                ap.active(False)
                sta = network.WLAN(network.STA_IF)
                sta.active(True)
                sta.connect(ssid, password)
                time.sleep(10)
                print(sta.ifconfig())
        break

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