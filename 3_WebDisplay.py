import machine
import ssd1306
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
i2c = machine.I2C(sda=machine.Pin(4), scl=machine.Pin(5))
display = ssd1306.SSD1306_I2C(64, 48, i2c)
def ToScreen(text):
    #3X
    h = 0
    while h < 3:
        i = 64
        while i > -100:
            display.fill(0)
            display.text(text,i,20)
            display.show()
            time.sleep(0.05)
            i -= 1
        h += 1
    display.show()
html = """<!DOCTYPE html><html><head><title>Morse Wi-Fi</title>
    <style type="text/css">#input{ color: #fff; text-align: center; margin: 10px; height: 30px; position: absolute; top:10%; left: 10%;}</style>
    </head><body><script type="text/javascript">
        function request(url) { var xhttp; if (window.XMLHttpRequest) { xhttp = new XMLHttpRequest(); } else { xhttp = new ActiveXObject("Microsoft.XMLHTTP"); } xhttp.onreadystatechange = function() { if (this.readyState == 4 && this.status == 200) { alert(this.responseText); } }; xhttp.open("GET", url, true); xhttp.send(); }
        function mudaLink(){ var text = document.getElementById('text'); request('Print='+text.value);}
    </script> <div id="input"><h4 color="#fff">Print in Display</h4><p><input id="text" type="text"/></p><p><button onclick="mudaLink();"> Enviar </button></p><p><button onclick="request('Print=ip');"> IP </button><button onclick="request('Print=mac');"> MAC </button><button onclick="request('Print=cpu');"> CPU </button></p>
    </div></body></html>"""
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
        linha = str(line)
        if not line or line == b'\r\n':
            cl.send(html)
            break 
        if not ure.search('Print', line):
            continue
        else:
            text = linha.split(' ')[1].split('=')[1]
            cl.send(html)
            if text == 'ip':
                ip = str(sta.ifconfig()).split('(')[1].split("'")[1]
                ToScreen(ip)
            elif text == 'mac':
                mac = '18:FE:39:CE:D3:26'
                ToScreen(mac)
            elif text == 'cpu':
                cpu = str(machine.freq())
                ToScreen(cpu)
            else:
                ToScreen(text)
        break
    cl.close()
