import network
import socket

def http_get(url):
    _, _, host, path = url.split('/', 3)
    addr = socket.getaddrinfo(host, 80)[0][-1]
    s = socket.socket()
    s.connect(addr)
    print('Socket connected!')
    s.send(bytes('GET /%s HTTP/1.0\\r\\nHost: %s\\r\\n\\r\\n' % (path, host), 'utf8'))
    while True:
        data = s.recv(100)
        if data:
            print(str(data, 'utf8'), end='')
        else:
            break

my_ap = 'RelaxenWatchenDasBlinkenlichten'
my_pw = 'murcielago1989'
print('Hello!')
wlan = network.WLAN(network.STA_IF)
wlan.connect(my_ap, my_pw)
print('Online!')
http_get('http://micropython.org/ks/test.html')
