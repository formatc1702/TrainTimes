import network\n
import usocket as socket\n
import ustruct as struct\n
import utime   as time\n
# import datetime\n
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
\n
\n
def get_time():\n
    NTP_DELTA = 3155673600 - 1 * 60 * 60 # Adjust for CET\n
    host = "pool.ntp.org"\n
    NTP_QUERY = bytearray(48)\n
    NTP_QUERY[0] = 0x1b\n
    addr = socket.getaddrinfo(host, 123)[0][-1]\n
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)\n
    s.settimeout(1)\n
    res = s.sendto(NTP_QUERY, addr)\n
    msg = s.recv(48)\n
    s.close()\n
    val = struct.unpack("!I", msg[40:44])[0]\n
    return val - NTP_DELTA\n
\n
def http_get(url,sta_index,nnnow):\n
    _, _, host, path = url.split('/', 3)\n
    addr = socket.getaddrinfo(host, 80)[0][-1]\n
    s = socket.socket()\n
    s.connect(addr)\n
    print("Socket connected!")\n
    s.send(bytes("GET /%s HTTP/1.0\\r\\nHost: %s\\r\\n\\r\\n" % (path, host), "utf8"))\n
    while True:\n
        line = s.readline()\n
        if line:\n
            if "<tr class=\"ivu_table_" in line:\n
                # extract relevant lines and clean them up\n
                departure_full_line = s.readline()\n
                departure_str = departure_full_line[12:17]\n
                s.readline()\n
                s.readline()\n
                s.readline()\n
                number_full_line = s.readline()\n
                number_str = number_full_line[8:-10]\n
                s.readline()\n
                s.readline()\n
                s.readline()\n
                direction_full_line = s.readline()\n
                # check if this train is actually relevant\n
                # iterate through all directions tram can go at one station\n
                for dir_index, direction in enumerate(directions):\n
                     # iterate through all destinations in that direction\n
                    for destination_want in direction:\n
                         # is the tram going where we want it to?\n
                        if destination_want in direction_full_line:\n
                            print(departure_str," : ",number_str," > ",direction_full_line)\n
                            now_tuple = time.localtime(nnnow)\n
                            # print(now_tuple)\n
                            departure = time.mktime((now_tuple[0],
                                                     now_tuple[1],
                                                     now_tuple[2],
                                                     int(departure_str[0:2]),
                                                     int(departure_str[3:5]),
                                                     0,0,0))\n
                            departure_tuple = time.localtime(departure)\n
                            print(departure_tuple)\n
                            difference = departure - now\n
                            # TODO: Check if end of day/month/year\n
                            print(difference)\n
                            # TODO: Remove connections that are inthe past
                            results[sta_index][dir_index] += [difference]\n
        else:\n
            break\n
\n
wifi_config = open("wificonfig.txt","r")\n
my_ap = wifi_config.readline().rstrip()\n
my_pw = wifi_config.readline().rstrip()\n
wifi_config.close()\n
print("Hello!")\n
wlan = network.WLAN(network.STA_IF)\n
wlan.connect(my_ap, my_pw)\n
print("Online!")\n
now = get_time()\n
print("Got current time!")\n
print(time.localtime(now))\n
for sta_index, station in enumerate(displays):\n
    url = "http://mobil.bvg.de/Fahrinfo/bin/stboard.bin/dox?input=" + station[0] + "&start=Suchen&boardType=depRT"\n
    # print(station[0])\n
    # print(url)\n
    directions = station[1:]\n
    http_get(url,sta_index,now)\n
\n
# TODO: Add padding with -999 at the end
for idx_station, station in enumerate(results):\n
    print(displays[idx_station][0])\n
    for direction in station:\n
        print (direction)\n
