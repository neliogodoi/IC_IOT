import machine, bme280, network, socket, time, ure

# FUNCTION TO RETURNS THE UNCERTANTYS OF SENSOR SETTING
def uncertantys(ovs, iir):
	a = 0.01 # Temp
	b = 0.0	 # Hum
	c = 0.0	 # Press

	if ovs == 1:
		b = 0.07
		if iir == 16:
			c = 0.4
		elif iir == 0:
			c = 3.3
	elif ovs == 2:
		b = 0.05
		if iir == 16:
			c = 0.4
		elif iir == 0:
			c = 2.6
	elif ovs == 3:
		b = 0.04
		if iir == 16:
			c = 0.3
		elif iir == 0:
			c = 2.1
	elif ovs == 4:
		b = 0.03
		if iir == 16:
			c = 0.2
		elif iir == 0:
			c = 1.6
	elif ovs == 5:
		b = 0.02
		if iir == 16:
			c = 0.2
		elif iir == 0:
			c = 1.3

	return (a, b, c)

# FUNCTION FOR BME280 SENSOR RE-SETTING
def setBME280(ovs, iir):
		bme = bme280.BME280(i2c=machine.I2C(sda=machine.Pin(4), scl=machine.Pin(5)), mode=ovs, iir=iir)

# FUNCTION PAGE HTML RETURNS
def page(ovs, iir):
	uncert = uncertantys(ovs, iir)
	temp, press, hum = bme.read_compensated_data()

	html = """<html><head><meta http-equiv='refresh' content='2'></head><body><script type='text/javascript'>function request(){var xhttp;if (window.XMLHttpRequest) { xhttp = new XMLHttpRequest(); } else { xhttp = new ActiveXObject('Microsoft.XMLHTTP');}xhttp.onreadystatechange = function() { if (this.readyState == 4 && this.status == 200) { alert('Fineshed'); } };var precision;var iir;var arrayPre = document.getElementsByName('selection');var arrayIir = document.getElementsByName('iir');for(var i = 0; i < arrayPre.length; i++){if(arrayPre[i].checked){precision = arrayPre[i].value;}}for(var i = 0; i < arrayIir.length; i++){if(arrayIir[i].checked){iir = arrayIir[i].value;}}xhttp.open('GET', '/presision='+precision+'='+iir, true);xhttp.send();}</script><h3>BME280 Sensor</h3>"""
	html += "Temperature : ("+"%.2f" %(temp / 100)+" +/- "+"%.2f" %uncert[0]+") C<br>"
	html += "Pressure : ("+"%.1f" %(press / 256)+" +/- "+"%.1f" %uncert[2]+") Pa<br>"
	html += "Humidity : ("+"%.2f" %(hum / 1024)+" +/- "+"%.2f" %uncert[1]+") %<br>"
	html += """<p>Oversampling : </p><input type='radio' name='selection' onclick='request()' value='1' checked>1x</input><input type='radio' name='selection' onclick='request()' value='2'>2x</input><input type='radio' name='selection' onclick='request()' value='3'>4x</input><input type='radio' name='selection' onclick='request()' value='4'>8x</input><input type='radio' name='selection' onclick='request()' value='5'>16x</input><p>Low pass filter : </p><input type='radio' name='iir' onclick='request()' value='16'>On</input><input type='radio' name='iir' onclick='request()' value='0' checked>Off</input></body></html>"""
	return html

# WIFI SETTINGS
ap = network.WLAN(network.AP_IF)
sta = network.WLAN(network.STA_IF)

'''
sta.active(False)
ap.active(True)
ap.config(essid='ESP', password='12345678') # Padrao
print(ap.ifconfig())
'''
# '''
ap.active(False)
sta.active(True)
sta.connect('Aquario', '642f2e396a')
while not sta.isconnected():
	time.sleep(1)
	print('.', end=' ')
print(sta.ifconfig())
# '''

# BME280 SENSOR SETTINGS
bme = bme280.BME280(i2c=machine.I2C(sda=machine.Pin(4), scl=machine.Pin(5)))
# SOCKET SETTINGS
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)
print('listening on', addr)

ovs = 1 # Oversample : off
iir = 0 # Low pass filter : off

while True:
	cl, addr = s.accept()
	print('client connected from', addr)
	cl_file = cl.makefile('rwb', 0)

	while True:
		line = cl_file.readline()
		linha = str(line)
		if not line or line == b'\r\n':
			respose = page(ovs, iir)
			try:
				cl.sendall(respose)
			except OSError:
				print('ERROR: Send Respose Failed !')
			break

		if not ure.search('presision', line):
			continue
		else:
			ovs = int(linha.split(' ')[1].split('=')[1])
			iir = int(linha.split(' ')[1].split('=')[2])
			print((ovs, iir))
			setBME280(ovs, iir)
			respose = page(ovs, iir)
			try:
				cl.sendall(respose)
			except OSError:
				print('ERROR: Send Respose Failed !')
			break
	cl.close()
