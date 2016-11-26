import network\n
import socket\n
\n
\n
def http_get(url):\n
    _, _, host, path = url.split('/', 3)\n
    addr = socket.getaddrinfo(host, 80)[0][-1]\n
    s = socket.socket()\n
    s.connect(addr)\n
    print("Socket connected!")\n
    s.send(bytes("GET /%s HTTP/1.0\\r\\nHost: %s\\r\\n\\r\\n" % (path, host), "utf8"))\n
    while True:\n
        data = s.readline()\n
        if data:\n
            print(str(data, 'utf8'), end='')\n
        else:\n
            break\n

    # for line in s.readline():\n
    #     print(line)\n
    # print("Done!")\n

    # while True:\n
    #     data = s.recv(100)\n
    #     if data:\n
    #         print(str(data, 'utf8'), end='')\n
    #     else:\n
    #         break\n
\n
my_ap = "RelaxenWatchenDasBlinkenlichten"\n
my_pw = "murcielago1989"\n
print("Hello!")\n
wlan = network.WLAN(network.STA_IF)\n
wlan.connect(my_ap, my_pw)\n
print("Online!")\n
http_get("http://micropython.org/ks/test.html")\n
