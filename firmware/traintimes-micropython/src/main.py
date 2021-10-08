# system modules
import esp
import gc
from machine import UART, Pin
import utime as time
# custom modules
from debugging import debug, debug_level, debug_free_memory
import ntp
import vbbapi
import wifi

PIN_BTN_SUMMERTIME = 4  # use switch on GPIO 4 (D2)
UART_ID = 1  # TX: GPIO2=D4, RX: none? (GPIO is also LED!)
UART_BAUDRATE = 9600

debug_free_memory(2)

# connect to WiFi
w = wifi.WiFi()

debug(1, 'Getting current time ', end='')
pin_summertime = Pin(PIN_BTN_SUMMERTIME, Pin.IN, Pin.PULL_UP)
if pin_summertime.value() == 0:  # swtich is pressed (low) = summertime
    summertime = True
    debug(1, 'using CEST...')
else:
    summertime = False
    debug(1, 'using CET...')

# get current time from NTP server
now = ntp.get_time(summertime)
debug(1, time.localtime(now))

debug(1, 'Connecting to VBB server...')
# connect to VBB API server
a = vbbapi.API()
def get_departures(origin, direction): # shorthand function
    return a.get_departures(origin, 5, direction, debug_level)

# configure the request
reqs = [
        ('Strassmannstr',      2,'Eberswalder'),
        ('Strassmannstr',      2,'Frankfurter_Tor'),
        ('S_Landsberger_Allee',5,'S_Gesundbrunnen'),
        ('S_Landsberger_Allee',5,'S_Neukolln'),
        ('S_Landsberger_Allee',5,'S_Bornholmer_Strasse'),
        ('S_Landsberger_Allee',5,'S_Schoneweide'),
        ('Bersarinplatz',      5,'Lichtenberg_Gudrunstr'),
        ('Bersarinplatz',      5,'Wilhelminenhofstr')
       ]
num_departures = 5

# read station IDs
debug(1, 'Reading station IDs...')
station_ids = {}
# check file for cached IDs
with open('stationids.txt','r') as f:
    while True:
        line = f.readline()
        if line:
            sid, sname = line.split(' ')
            station_ids[sname.strip()] = sid.strip()
            debug(2, f'ID {sid.strip()} is {sname.strip()}')
        else:
            break
# get missing IDs from API
for origin, walktime, direction in reqs:
    if not origin in station_ids:
        station_ids[origin]    = a.get_station_id(origin)
        debug(2, f'New ID {station_ids[origin]} is {origin}')
    if not direction in station_ids:
        station_ids[direction] = a.get_station_id(direction)
        debug(2, f'New ID {station_ids[direction]} is {direction}')
# finished
debug(1, 'Got all station IDs.')

# free up some memory?
gc.collect()
debug_free_memory(2)

# get departure times
debug(1, 'Getting departure times...')
out = []
for origin, walktime, direction in reqs: # iterate over each origin/direction tuple
    debug(2, f'{origin} -> {direction}')
    # request departure times from API
    departures = get_departures(station_ids[origin], station_ids[direction])
    _out = []
    for t in departures: # iterate over each received departure time
        # how much until departure?
        timediff = t - now
        debug(2, t, time.localtime(t), timediff,
                  'departs in {: 03}:{:02}'.format(timediff // 60, timediff % 60))
        # should we keep this departure?
        if timediff > 0: # is it in the future?
            if timediff < 99 * 60: # is it in the next 99 mins but at least 2 min in future?
                if timediff > walktime * 60:
                    _out.append(timediff)
            else: # add placeholder if not
                _out.append('-999')
    # add placeholders for padding
    if len(_out) < num_departures:
        for i in range(len(_out), num_departures):
            _out.extend(['-999'])
    # add to list
    out.append(_out)

    gc.collect()
    debug_free_memory(2)

# Output data to Arduino
debug(1, '')
debug(1, 'Sending data to UART...', end='')
uart = UART(UART_ID, UART_BAUDRATE)
time.sleep(0.1)
uart.write('{')
uart.write('\n')
for dirs in out:
    for deps in dirs:
        uart.write(f'{deps} \n')
    time.sleep(0.05) # give Arduino time to read the buffer
uart.write('}')
uart.write('\n')
uart.write('\n')
debug(1, ' done.')

debug(2, '')
debug(2, 'UART payload:')
for dirs in out:
    for deps in dirs:
        debug(2, f'{deps}\t', end='')
    debug(2, '')
debug(2, '')

debug(1, 'Finished!')

if not debug_level:
    debug(0, 'Sleeping...')
    w.wlan.active(False)
    esp.deepsleep()
else:
    debug(1, f'Not sleeping (debug level {debug_level})')
    debug(1, '')
