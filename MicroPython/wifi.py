import network
from time import sleep

class WiFi():
    def __init__(self):
        wifi_config = open("wificonfig.txt","r")
        my_ap = wifi_config.readline().rstrip()
        my_pw = wifi_config.readline().rstrip()
        wifi_config.close()
        print("SSID: ", my_ap)
        print("PWD:  ", my_pw)

        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        self.wlan.connect(my_ap, my_pw)

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
