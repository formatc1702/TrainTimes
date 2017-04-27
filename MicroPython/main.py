import wifi
import http
import vbbapi

w = wifi.WiFi()
a = vbbapi.API()

sid     = a.get_station_id("Strassmannstr")
dirid_n = a.get_station_id("Eberswalder")
dirid_s = a.get_station_id("Bersarinplatz")

print(sid)
print(dirid_n)
print(dirid_s)

dep_n = a.get_departures(sid, 1, dirid_n)
dep_s = a.get_departures(sid, 1, dirid_s)

print(dep_n)
print(dep_s)
