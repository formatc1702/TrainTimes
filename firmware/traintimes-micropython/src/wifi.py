import network
from time import sleep

from debugging import debug

class WiFi():
    def __init__(self):
        with open('wificonfig.txt','r') as f:
            self.ssid = f.readline().rstrip()
            self.pw   = f.readline().rstrip()

        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)

        debug(1, f'Connecting to WiFi "{self.ssid}"', end='')
        self.wlan.connect(self.ssid, self.pw)

        for i in range(0,60): # attempt to connect
            ip, mask, gateway, dns = self.wlan.ifconfig()
            if ip == 0.0.0.0: #not connected
                debug(1, '.', end='')
                sleep(1)
            else: #connected!
                debug(1, '')
                debug(1, f'Connected with IP {ip}')
                break
        else:
            debug(0, 'ERROR: Could not connect to WiFi')
