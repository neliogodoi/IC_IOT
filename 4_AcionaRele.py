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
light = Pin(5, Pin.OUT)
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)
print('listening on', addr)

html = """<!DOCTYPE html>
    <html>
    <head>
    <title>Interruptor Wi-Fi</title>
    <style type="text/css">
    body{ background-color: #fc0;} 
    #Lampada{ margin: 2px solid ; height: 30px; position: absolute; left: 30%;}
    </style>
    </head>
    <body>
    <script type="text/javascript">
        function request(url) {
          var xhttp;
          if (window.XMLHttpRequest) {
            xhttp = new XMLHttpRequest();
            } else {
            xhttp = new ActiveXObject("Microsoft.XMLHTTP");
          }
          xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
              alert('Finished!');
            }
          };
          xhttp.open("GET", url, true);
          xhttp.send();
        }
    </script>
    <div id="Lampada"></h1>
    <button type="submit" onclick="request('LightStatus=On');">Ligar</button>
    <button type="submit" onclick="request('LightStatus=Off');">Desligar</button> </div></body>
    </html>
    """

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
