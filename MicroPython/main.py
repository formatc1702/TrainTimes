# system modules
import utime as time
import gc
# custom modules
import wifi
import ntp
import vbbapi
from machine import UART

# connect to WiFi
w = wifi.WiFi()

# get current time from NTP server
now = ntp.get_time()
print(time.localtime(now))

# connect to VBB API server
a = vbbapi.API()
def get_departures(origin, direction): # shorthand function
    return a.get_departures(origin, 5, direction, False)

# configure the request
reqs = [
        ("Strassmannstr",      2, "Eberswalder"),
        ("Strassmannstr",      2, "Frankfurter_Tor"),
        ("S_Landsberger_Allee",5,"S_Gesundbrunnen"),
        ("S_Landsberger_Allee",5,"S_Neukolln"),
        ("S_Landsberger_Allee",5,"S_Bornholmer_Strasse"),
        ("S_Landsberger_Allee",5,"S_Schoneweide"),
        ("Bersarinplatz",      5,"Lichtenberg_Gudrunstr"),
        ("Bersarinplatz",      5,"Wilhelminenhofstr")
       ]
num_departures = 5

# read station IDs
station_ids = {}
# check file for cached IDs
with open("stationids.txt","r") as f:
    while True:
        line = f.readline()
        if line:
            sid, sname = line.split(' ')
            station_ids[sname.strip()] = sid.strip()
            print("ID {} is {}".format(sid.strip(), sname.strip()))
        else:
            break
# get missing IDs from API
for origin, walktime, direction in reqs:
    if not origin in station_ids:
        station_ids[origin]    = a.get_station_id(origin)
        print("New ID {} is {}".format(station_ids[origin],    origin))
    if not direction in station_ids:
        station_ids[direction] = a.get_station_id(direction)
        print("New ID {} is {}".format(station_ids[direction], direction))
# finished
print("Got all IDs!")

# free up some memory?
gc.collect()
print(gc.mem_free())

# get departure times
out = []
for origin, direction in reqs: # iterate over each origin/direction tuple
    print("{} -> {}".format(origin, direction))
    # request departure times from API
    departures = get_departures(station_ids[origin], station_ids[direction])
    _out = []
    for t in departures: # iterate over each received departure time
        # how much until departure?
        timediff = t - now
        print(t, time.localtime(t), timediff,
              "departs in {: 03}:{:02}".format(timediff // 60, timediff % 60))
        # should we keep this departure?
        if timediff > 0: # is it in the future?
            if timediff < 99 * 60: # is it in the next 99 mins but at least 2 min in future?
                if timediff > walktime * 60:
                    _out.append(timediff)
            else: # add placeholder if not
                _out.append("-999")
    # add placeholders for padding
    if len(_out) < num_departures:
        for i in range(len(_out), num_departures):
            _out.extend(["-999"])
    # add to list
    out.append(_out)

    gc.collect()
    print(gc.mem_free())

# Output data to Arduino
uart = UART(1,9600) # TX: GPIO2=D4, RX: none? (GPIO is also LED!)
uart.write("")
uart.write("{")
for dirs in out:
    for deps in dirs:
        uart.write("{:>4} \t".format(deps))
        print     ("{:>4} \t".format(deps), end="")
    print("")
uart.write("}")
