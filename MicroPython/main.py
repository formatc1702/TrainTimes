import gc

import wifi
import ntp
import utime as time
import vbbapi

w = wifi.WiFi()

now = ntp.get_time()
print(time.localtime(now))

a = vbbapi.API()
sid     = a.get_station_id("Strassmannstr")
dirid_n = a.get_station_id("Eberswalder")
dirid_s = a.get_station_id("Bersarinplatz")

n_t = a.get_departures(sid, 5, dirid_n, True)
for t in n_t:
    print(t, time.localtime(t), "departs in {:+03}:{:02}".format((t - now) // 60, (t - now) % 60))

s_t = a.get_departures(sid, 5, dirid_s, True)
for t in s_t:
    print(t, time.localtime(t), "departs in {:+03}:{:02}".format((t - now) // 60, (t - now) % 60))
