import network
import usocket as socket
import ustruct as struct
import utime   as time
from machine import UART, Pin # connect D4 pin (TX) to RX line on the display
# import datetime
# from datetime import datetime

debug_mode = False

led = Pin(2)
led.init(Pin.OUT)
led.high() # LED off

def blink_on(times):
    for i in range(0,times):
        led.low()
        time.sleep(0.25)
        led.high()
        time.sleep(0.25)

def debug(*args,**kwargs):
    if debug_mode == True:
        print(*args,**kwargs)

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

def http_get(url,sta_index,nnnow):
    _, _, host, path = url.split('/', 3)
    addr = socket.getaddrinfo(host, 80)[0][-1]
    s = socket.socket()
    s.connect(addr)
    debug("Socket connected!")
    s.send(bytes("GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n" % (path, host), "utf8"))
    while True:
        line = s.readline()
        if line:
            if "<tr class=\"ivu_table_" in line:
                # extract relevant lines and clean them up
                departure_full_line = s.readline()
                # print(" ")
                # print(departure_full_line)
                departure_str = departure_full_line[12:17]
                s.readline()
                s.readline()
                s.readline()
                number_full_line = s.readline()
                # print(number_full_line)
                number_str = number_full_line[8:-10]
                s.readline()
                s.readline()
                s.readline()
                direction_full_line = s.readline()
                # print(direction_full_line)
                if "<td>" in direction_full_line:
                    direction_full_line = s.readline()
                    # print("->",direction_full_line)
                # check if this train is actually relevant
                # iterate through all directions tram can go at one station
                for dir_index, direction in enumerate(directions):
                     # iterate through all destinations in that direction
                    for destination_want in direction:
                         # is the tram going where we want it to?
                        if destination_want in direction_full_line:
                            debug(departure_str," : ",number_str," > ",direction_full_line)
                            now_tuple = time.localtime(nnnow)
                            # print(now_tuple)
                            departure = time.mktime((now_tuple[0],
                                                     now_tuple[1],
                                                     now_tuple[2],
                                                     int(departure_str[0:2]),
                                                     int(departure_str[3:5]),
                                                     0,0,0))
                            departure_tuple = time.localtime(departure)
                            debug(departure_tuple)
                            difference = departure - now
                            # TODO: Check if end of day/month/year
                            if   difference >= 60:
                                results[sta_index][dir_index] += [difference]
                                debug(difference)
                            elif difference <= 0: # avoid sending a 0 (breaks the ParseInt function on Arduino side)
                                debug(difference, "<60")
                            else:
                                debug(difference, "<=0")
        else:
            break

wifi_config = open("wificonfig.txt","r")
my_ap = wifi_config.readline().rstrip()
my_pw = wifi_config.readline().rstrip()
wifi_config.close()
debug("Hello!")
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
debug("SSID: ", my_ap)
debug("PWD:  ", my_pw)

wlan.connect(my_ap, my_pw)
for i in range(0,40): # attempt to connect
    ip,mask,gateway,dns = wlan.ifconfig()
    if ip == "0.0.0.0": #not connected
        debug(".")
        time.sleep(1)
    else: #connected!
        debug("Got IP: ", ip)
        blink_on(2)
        now = get_time()
        debug("Got current time: ", time.localtime(now))
        for sta_index, station in enumerate(displays):
            led.high()
            url = "http://mobil.bvg.de/Fahrinfo/bin/stboard.bin/dox?input=" + station[0] + "&start=Suchen&boardType=depRT"
            # print(station[0])
            # print(url)
            directions = station[1:]
            http_get(url,sta_index,now)
            led.low()

        wlan.disconnect()

        uart = UART(1,9600) # TX: GPIO2=D4, RX: none? (GPIO is also LED!)
        # uart = UART(2,9600) # TX: GPIO15=D8, RX: GPIO13=D7, not implemented?

        uart.write('{')
        uart.write('\n')
        for idx_station, station in enumerate(results):
            debug(displays[idx_station][0])
            for direction in station:
                n = len(direction)
                if n > 5:
                    direction = direction[0:5]
                if n < 5:
                    for i in  range(n,5):
                        direction += [-999]
                debug (direction)
                debug (len(direction))
                uart.write(str(direction))
                uart.write('\n')
        uart.write('}')
        uart.write('\n')
        uart.write('\n')
        time.sleep(1)
        led.init(Pin.OUT)
        led.low()
        time.sleep(2)
        led.high()
        debug("Finished!")
        break
else:
    print("Could not connect to WiFi")
