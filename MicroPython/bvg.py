import network
import usocket as socket
import ustruct as struct
import utime   as time
# import datetime
# from datetime import datetime

displays = [
    ["Strassmannstr",
        ["Friedrich-Ludwig-Jahn-Sportpark", "S+U Hauptbahnhof"],
        ["S+U Warschauer Str."]]
    ,
    ["S+Landsberger+Allee+%28Berlin%29",
        ["Ringbahn S 42"],
        ["Ringbahn S 41"],
        ["S Blankenburg (Berlin)","S+U Pankow (Berlin)","S Birkenwerder Bhf"],
        ["S Flughafen Berlin-Sch&#246;nefeld Bhf","Sch&#246;neweide","S Gr&#252;nau (Berlin)"]]
    ,
    ["Bersarinplatz",
        ["Lichtenberg"],
        ["Sch&#246;neweide"]]
    ]

results = [[[],[]],[[],[],[],[]],[[],[]]]

def get_time():
    NTP_DELTA = 3155673600 - 1 * 60 * 60 # Adjust for CET
    host = "pool.ntp.org"
    NTP_QUERY = bytearray(48)
    NTP_QUERY[0] = 0x1b
    addr = socket.getaddrinfo(host, 123)[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(1)
    res = s.sendto(NTP_QUERY, addr)
    msg = s.recv(48)
    s.close()
    val = struct.unpack("!I", msg[40:44])[0]
    return val - NTP_DELTA

def http_get(url,sta_index,nnnow,dirs):
    _, _, host, path = url.split('/', 3)
    addr = socket.getaddrinfo(host, 80)[0][-1]
    s = socket.socket()
    s.connect(addr)
    print("Socket connected!")
    s.send(bytes("GET /%s HTTP/1.0\\r\\nHost: %s\\r\\n\\r\\n" % (path, host), "utf8"))
    while True:
        line = s.readline()
        if line:
            if "<tr class=\"ivu_table_" in line:
                # extract relevant lines and clean them up
                departure_full_line = s.readline()
                print(departure_full_line)
                departure_str = departure_full_line[12:17]
                s.readline()
                s.readline()
                s.readline()
                number_full_line = s.readline()
                print(number_full_line)
                if "<td>" in number_full_line:
                    number_full_line = s.readline()
                    print("->",number_full_line)
                number_str = number_full_line[8:-10]
                s.readline()
                s.readline()
                s.readline()
                direction_full_line = s.readline()
                print(direction_full_line)
                # check if this train is actually relevant
                # iterate through all directions tram can go at one station
                for dir_index, direction in enumerate(dirs):
                     # iterate through all destinations in that direction
                    for destination_want in direction:
                         # is the tram going where we want it to?
                        if destination_want in direction_full_line:
                            print(departure_str," : ",number_str," > ",direction_full_line)
                            now_tuple = time.localtime(nnnow)
                            # print(now_tuple)
                            departure = time.mktime((now_tuple[0
                                                     now_tuple[1
                                                     now_tuple[2
                                                     int(departure_str[0:2]
                                                     int(departure_str[3:5]
                                                     0,0,0))
                            departure_tuple = time.localtime(departure)
                            print(departure_tuple)
                            difference = departure - now
                            # TODO: Check if end of day/month/year
                            print(difference)
                            # TODO: Remove connections that are inthe past
                            results[sta_index][dir_index] += [difference]
        else:
            break

wifi_config = open("wificonfig.txt","r")
my_ap = wifi_config.readline().rstrip()
my_pw = wifi_config.readline().rstrip()
wifi_config.close()
print("Hello!")
wlan = network.WLAN(network.STA_IF)
wlan.connect(my_ap, my_pw)
print("Online!")
now = get_time()
print("Got current time!")
print(time.localtime(now))
for sta_index, station in enumerate(displays):
    url = "http://mobil.bvg.de/Fahrinfo/bin/stboard.bin/dox?input=" + station[0] + "&start=Suchen&boardType=depRT")
    # print(station[0])
    # print(url)
    directions = station[1:]
    http_get(url,sta_index,now,directions)

# TODO: Add padding with -999 at the end
for idx_station, station in enumerate(results):
    print(displays[idx_station][0])
    for direction in station:
        print (direction)

wlan.disconnect()
