import gc

print(gc.mem_free())


import wifi
print(gc.mem_free())
import http
print(gc.mem_free())
import vbbapi

print(gc.mem_free())

w = wifi.WiFi()
print(gc.mem_free())
a = vbbapi.API()

print(gc.mem_free())
gc.collect()
print(gc.mem_free())

sid     = a.get_station_id("Strassmannstr")
print("SID",sid)
print(gc.mem_free())
dirid_n = a.get_station_id("Eberswalder")
print("DIRN",dirid_n)
print(gc.mem_free())
dirid_s = a.get_station_id("Bersarinplatz")
print("DIRS",dirid_s)
print(gc.mem_free())


print(gc.mem_free())

dep_n = a.get_departures(sid, 5, dirid_n)
dep_s = a.get_departures(sid, 5, dirid_s)

print(dep_n)
print(dep_s)

print(gc.mem_free())
