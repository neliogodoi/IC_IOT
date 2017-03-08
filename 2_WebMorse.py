from machine import Pin
import webrepl
import socket
import time
import network
import ure
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.connect('PERNINHA', 'Manicomiof4022')
sta.ifconfig()
webrepl.start()
led = Pin(2, Pin.OUT)
led.value(1)

def piscaMorse(numero):
    i = 0
    print(len(numero))
    while i < len(numero):
        print(i)
        for j in morse(numero[i]):
            if j == 0:
                led.value(0)
                time.sleep(1)
                led.value(1)
                time.sleep(0.3)
            else:
                led.value(0)
                time.sleep(0.3)
                led.value(1)
                time.sleep(0.3)
        time.sleep(3)
        i+=1
       
def morse(k):
    if k == '1':
        return [1, 0, 0, 0, 0]
    elif k == '2':
        return [1, 1, 0, 0, 0]
    elif k == '3':
        return [1, 1, 1, 0, 0]
    elif k == '4':
        return [1, 1, 1, 1, 0]
    elif k == '5':
        return [1, 1, 1, 1, 1]
    elif k == '6':
        return [0, 1, 1, 1, 1]
    elif k == '7':
        return [0, 0, 1, 1, 1]
    elif k == '8':
        return [0, 0, 0, 1, 1]
    elif k == '9':
        return [0, 0, 0, 0, 1]
    else:
        return [0, 0, 0, 0, 0]
        
html = """<!DOCTYPE html> <html> <head>
    <title>Morse Wi-Fi</title> <style type="text/css">
    #input{ align-text: center; margin: 10px; height: 30px; position: absolute; top: 30%; left: 20%;}
    </style> </head> <body> <script type="text/javascript">
    function mudaLink(){ var numero = document.getElementById('numero'); document.getElementById('link').href="MorseOf="+numero.value;}
    </script> <div id="input">
    <h4 color="#fff">Web Morse in Wemos D1 mini</h4>
    <input id="numero" type="text"/><p> </p><a id="link" href=""><button type="submit" onclick="mudaLink();">Enviar</button></a>        
    </div> </body> </html>"""

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)
print('listening on', addr)

while True:
    cl, addr = s.accept()
    print('client connected from', addr)
    cl_file = cl.makefile('rwb', 0)

    while True:
        line = cl_file.readline()
        #Problemas: Necessita converçao da line para string
        # para fazer o .split()
        linha = str(line)
        if not line or line == b'\r\n':
            cl.send(html)
            break 
        if not ure.search('MorseOf', line):
            continue
        else:
            numero = linha.split(' ')[1].split('=')[1]
            cl.send(html)
            piscaMorse(numero)
        break
    led.value(1)
    cl.close()
