import network\n
import socket\n
# from datetime import datetime\n
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
def http_get(url,sta_index):\n
    _, _, host, path = url.split('/', 3)\n
    addr = socket.getaddrinfo(host, 80)[0][-1]\n
    s = socket.socket()\n
    s.connect(addr)\n
    print("Socket connected!")\n
    s.send(bytes("GET /%s HTTP/1.0\\r\\nHost: %s\\r\\n\\r\\n" % (path, host), "utf8"))\n
    while True:\n
        line = s.readline()\n
        if line:\n
            if line.startswith('Date:'):\n
                date_str = line[6:-1]\n
                # print(date_str)                     # Sat, 26 Nov 2016 20:23:09 GMT\n
                # date_obj = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %Z')\n
                # print(date_obj.hour)\n
                # print(date_obj.minute)\n
                # print(date_obj.second)\n
            else:\n
                for dir_index, direction in enumerate(directions): # iterate through all directions tram can go at one station\n
                    for destination_want in direction: # iterate through all destinations in that direction\n
                        if destination_want in line: # is the tram going where we want it to?\n
                            # print str(dir_index) + '...' + line.rstrip() + '...' + destination_want\n
                            s.readline()\n
                            s.readline()\n
                            s.readline()\n
                            # print response.readline()\n
                            results[sta_index][dir_index] += [s.readline()[12:17]]\n
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
# \n
# bla = ['a','b','c']\n
# for idx,blu in enumerate(bla):\n
#     print(blu)\n
# \n
for sta_index, station in enumerate(displays):\n
    url = "http://mobil.bvg.de/Fahrinfo/bin/stboard.bin/dox?input=" + station[0] + "&start=Suchen&boardType=depRT"\n
    print(station[0])\n
    print(url)\n
    directions = station[1:]\n
    http_get(url,sta_index)\n
\n
for idx_station, station in enumerate(results):\n
    print(displays[idx_station][0])\n
    for direction in station:\n
        print (direction)\n
