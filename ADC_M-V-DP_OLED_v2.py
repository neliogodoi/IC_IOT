import machine, time, ssd1306

adc = machine.ADC(0)
MAX = 5
NumElem = 100

i2c = machine.I2C(sda=machine.Pin(4), scl=machine.Pin(5))
display = ssd1306.SSD1306_I2C(64, 48, i2c)

while 1:
	display.fill(0)
	display.text("...",20,22)
	display.show()

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

	media = total/MAX

	TotalVar = 0
	for i in range(len(amostra)):
		TotalVar += TotalVar + ((amostra[i]-media)**2)

	Variancia = TotalVar/MAX
	DesvioPadrao = Variancia**(1/2)

	display.fill(0)
	display.text("[%.2f]" %media, 1, 5)
	display.text("[%.2f]" %Variancia, 1, 24)
	display.text("[%.2f]" %DesvioPadrao, 1, 35)
	display.show()
	time.sleep(5)

