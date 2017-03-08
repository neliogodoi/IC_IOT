# Easy code for selection AP or STA mode on ESP8266
import machine
import network
import socket
import time
import dht

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid='ESP', password='12345678')

DHT = dht.DHT22(machine.Pin(2))
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)
print('listening on', addr)

while True:
	time.sleep(2)
	cl, addr = s.accept()
	print('client connected from', addr)
	cl_file = cl.makefile('rwb', 0)
	while True:
		line = cl_file.readline()
		if not line or line == b'\r\n':
			break
	DHT.measure()
	t = str(DHT.temperature())
	h = str(DHT.humidity())
	html = "<!DOCTYPE html><html><head><meta http-equiv='refresh' content='2'></head><body>"
	html += "Temperatura: "+int(t)+" *C<br>"
	html += "Humidade: "+int(h)+" %"
	html += "</body></html>"
	cl.send(html)
	cl.close()
    