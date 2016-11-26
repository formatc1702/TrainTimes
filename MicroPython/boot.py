import network\n
import socket\n
\n
displays = [\n
    ["Strassmannstr",\n
        ["Friedrich-Ludwig-Jahn-Sportpark", "S+U Hauptbahnhof"],\n
        ["S+U Warschauer Str."]]\n
    ,\n
    ["S+Landsberger+Allee+%28Berlin%29",\n
        ["Ringbahn S 42"],\n
        ["Ringbahn S 41"],\n
        ["S Blankenburg (Berlin)","S+U Pankow (Berlin)","S Birkenwerder Bhf"],\n
        ["S Flughafen Berlin-Sch&#246;nefeld Bhf","Sch&#246;neweide","S Gr&#252;nau (Berlin)"]]\n
    ,\n
    ["Bersarinplatz",\n
        ["Lichtenberg"],\n
        ["Sch&#246;neweide"]]\n
    ]\n
\n
results = [[[],[]],[[],[],[],[]],[[],[]]]\n
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
for staindex, station in enumerate(displays):\n
    url = "http://mobil.bvg.de/Fahrinfo/bin/stboard.bin/dox?input=" + station[0] + "&start=Suchen&boardType=depRT"\n
    print station[0]\n
    print url\n
    directions = station[1:]\n
    http_get(url)\n
