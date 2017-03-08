import machine, time
adc = machine.ADC(0)
while 1:
	total = 0
	for i in range(100):
		total = total + adc.read()
		time.sleep_ms(50)

	media = total/100
	v = (media*3.3)/1023
	print("Medias 100 leituras: ADC: "+str(media)+", Volts: %.2f" %v)
