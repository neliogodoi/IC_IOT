# Easy code for selection AP or STA mode on ESP8266
import machine
import ure
import network
import socket
import time
import dht

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid='ESP', password='12345678')


DHT = dht.DHT22(machine.Pin(2))
light = machine.Pin(5, machine.Pin.OUT);

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

    DHT.measure()

    if(DHT.humidity() < 60.0):
        light.value(0)
    if(DHT.humidity() > 80.0):
        light.value(1)    


    t = str(DHT.temperature())
    h = str(DHT.humidity())

    html = """<!DOCTYPE html>
    <html>
    <head>
    <title>Interruptor Wi-Fi</title>
    <style type="text/css">
    body{ background-color: #fc0;} 
    #Lampada{ margin: 2px solid ; height: 30px; position: absolute; left: 30%;}
    </style>
    <meta http-equiv='refresh' content='2'>
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
    <button type="submit" onclick="request('LightStatus=Off');">Desligar</button> </div>
    """
    html += "<div id='dht'>Temperatura: "+t+" *C<br>"
    html += "Humidade: "+h+" %"
    html += "</div></body></html>"

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

    