import network
from time import sleep

class WiFi():
    def __init__(self):
        with open("wificonfig.txt","r") as f:
            self.ssid = f.readline().rstrip()
            self.pw   = f.readline().rstrip()

        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        self.wlan.connect(self.ssid, self.pw)

        for i in range(0,60): # attempt to connect
            ip, mask, gateway, dns = self.wlan.ifconfig()
            if ip == "0.0.0.0": #not connected
                print(".")
                sleep(1)
            else: #connected!
                print("Got IP: ", ip)
                break
        else:
            print("ERROR: Could not connect to WiFi")
