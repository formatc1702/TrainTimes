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
for origin, direction in reqs:
    if not origin in sids:
        sids[origin] = a.get_station_id(origin)
        print("Got ID for {}: {}".format(origin, sids[origin]))
    if not direction in sids:
        sids[direction] = a.get_station_id(direction)
        print("Got ID for {}: {}".format(direction, sids[direction]))

sids["Bersarinplatz"] = "9120816" # Bersarin (Weidenweg) can't be found by location.name?
print("Got all IDs!")

gc.collect()
print(gc.mem_free())

for origin, direction in reqs:
    print(origin, direction)
    departures = get_departures(sids[origin], sids[direction])
    for t in departures:
        print(t, time.localtime(t), "departs in {:+03}:{:02}".format((t - now) // 60, (t - now) % 60))
    gc.collect()
    print(gc.mem_free())
