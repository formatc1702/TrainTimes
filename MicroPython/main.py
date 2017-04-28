import gc

import wifi
print(gc.mem_free())
import vbbapi

w = wifi.WiFi()
a = vbbapi.API()
sid     = a.get_station_id("Strassmannstr", True)
print("SID",sid)
dirid_n = a.get_station_id("Eberswalder", True)
print("DIRN",dirid_n)
dirid_s = a.get_station_id("Bersarinplatz", True)
print("DIRS",dirid_s)

n_d, n_t = a.get_departures(sid, 5, dirid_n)
print(n_d, n_t)

s_d, s_t = a.get_departures(sid, 5, dirid_s)
print(s_d, s_t)
