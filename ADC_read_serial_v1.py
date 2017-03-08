import machine, time
adc = machine.ADC(0)
while True:
	val = adc.read()
	v = (val*3.3)/1023
	print("ADC: "+str(val)+" , Volts: %.2f" %v)
	time.sleep_ms(500)
