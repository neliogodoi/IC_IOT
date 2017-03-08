import machine, network, socket, time

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid='nelio')#, password='12345678')

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)
print('listening on', addr)

def MVDP():
	adc = machine.ADC(0)
	MAX = 5
	NumElem = 100

	amostra = []
	media = 0 
	Variancia = 0
	DesvioPadrao = 0

	for j in range(MAX):
		total = 0
		for i in range(NumElem):
			total += adc.read()
			time.sleep_ms(10)
		amostra.append(total/NumElem)

	total = 0
	for i in range(len(amostra)):
		total += amostra[i]

	Media = total/MAX

	TotalVar = 0
	for i in range(len(amostra)):
		TotalVar += TotalVar + ((amostra[i]-Media)**2)

	Variancia = TotalVar/MAX
	DesvioPadrao = Variancia**(1/2)

	return (Media, Variancia, DesvioPadrao)

while True:
	time.sleep(2)
	cl, addr = s.accept()
	print('client connected from', addr)
	cl_file = cl.makefile('rwb', 0)
	while True:
		line = cl_file.readline()
		if not line or line == b'\r\n':
			break

	mvdp = MVDP()

	html = "<!DOCTYPE html><html><head><meta http-equiv='refresh' content='2'></head><body>"
	html += "<h3>ADC WebServer</h3><p>500 leituras<p>"
	html += "Media: [ADC: "+str(mvdp[0])+", Volts: "+str((mvdp[0]*3.3)/1023)+"]<br>"
	html += "Variancia: "+str(mvdp[1])+"<br>Desvio Padrao: "+str(mvdp[2])
	html += "</body></html>"

	cl.sendall(html)
	cl.close()