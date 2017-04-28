import gc

import wifi
import ntp
import utime as time
import vbbapi

w = wifi.WiFi()

now = ntp.get_time()
print(time.localtime(now))

a = vbbapi.API()
def get_departures(origin, direction):
    return a.get_departures(origin, 5, direction, True)

num_departures = 5

reqs = [
        ("Strassmannstr",      "Eberswalder"),
        ("Strassmannstr",      "Frankfurter_Tor"),
        ("S_Landsberger_Allee","S_Gesundbrunnen"),
        ("S_Landsberger_Allee","S_Neukolln"),
        ("S_Landsberger_Allee","S_Bornholmer_Strasse"),
        ("S_Landsberger_Allee","S_Schoneweide"),
        ("Bersarinplatz",      "Lichtenberg_Gudrunstr"),
        ("Bersarinplatz",      "Wilhelminenhofstr")
       ]

sids = {}

with open("stationids.txt","r") as f:
    while True:
        line = f.readline()
        if line:
            sid, sname = line.split(' ')
            sids[sname.strip()] = sid.strip()
            print("ID {} is {}".format(sid.strip(), sname.strip()))
        else:
            break


for origin, direction in reqs:
    if not origin in sids:
        sids[origin] = a.get_station_id(origin)
        print("Got ID for {}: {}".format(origin, sids[origin]))
    if not direction in sids:
        sids[direction] = a.get_station_id(direction)
        print("Got ID for {}: {}".format(direction, sids[direction]))

print("Got all IDs!")

gc.collect()
print(gc.mem_free())

out = []
for origin, direction in reqs:
    print("{} -> {}".format(origin, direction))
    departures = get_departures(sids[origin], sids[direction])
    _out = []
    for t in departures:
        timediff = t - now
        print(t, time.localtime(t), timediff,  "departs in {:+03}:{:02}".format(timediff // 60, timediff % 60))

        if timediff > 0:
            if timediff < 99 * 60:
                _out.append(timediff)
            else: # can't display more than 99 mins
                _out.append("-999")

    if len(_out) < num_departures:
        for i in range(len(_out), num_departures):
            _out.extend(["-999"])

    out.append(_out)
    gc.collect()
    print(gc.mem_free())

# print(out)

print("")
print("{")
for dirs in out:
    for deps in dirs:
        print("{:>4} \t".format(deps), end="")
    print("")
print("}")
