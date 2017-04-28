import gc

import wifi
import ntp
import utime as time
import vbbapi

w = wifi.WiFi()

now = ntp.get_time()
print(time.localtime(now))

a = vbbapi.API()

def get_station_ids(stations):
    ids = {}
    for s in stations:
        ids[s] = a.get_station_id(s, True)
    return ids

def get_departures(origin, direction):
    # oid = a.get_station_id(origin)
    # did = a.get_station_id(direction)

    return a.get_departures(origin, 5, direction, True)

stations = ["Strassmannstr",
            "Frankfurter_Tor",
            "Eberswalder",

            "S_Landsberger_Allee",
            "S_Gesundbrunnen",
            "S_Neukolln",
            "S_Bornholmer_Strasse",
            "S_Schoneweide",

            "Bersarinplatz",
            "Lichtenberg_Gudrunstr",
            "Wilhelminenhofstr",
            ]

sids = get_station_ids(stations)
sids["Bersarinplatz"] = "9120816"
print(sids)
gc.collect()
print(gc.mem_free())

reqs = [
        ("Strassmannstr",      "Frankfurter_Tor"),
        ("Strassmannstr",      "Eberswalder"),
        ("S_Landsberger_Allee","S_Gesundbrunnen"),
        ("S_Landsberger_Allee","S_Neukolln"),
        ("S_Landsberger_Allee","S_Bornholmer_Strasse"),
        ("S_Landsberger_Allee","S_Schoneweide"),
        ("Bersarinplatz",      "Lichtenberg_Gudrunstr"),
        ("Bersarinplatz",      "Wilhelminenhofstr")
       ]

for origin, direction in reqs:
    print(origin, direction)
    departures = get_departures(sids[origin], sids[direction])
    for t in departures:
        print(t, time.localtime(t), "departs in {:+03}:{:02}".format((t - now) // 60, (t - now) % 60))
    gc.collect()
    print(gc.mem_free())
