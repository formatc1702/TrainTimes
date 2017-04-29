import socket
import machine

import wifi

w = wifi.WiFi()

#HTML to send to browsers
html = """<!DOCTYPE html>
<html>
<head> <title>ESP8266 LED ON/OFF</title> </head>
<center><h2>A simple webserver for turning HUZZAH Feather LED's on and off with Micropython</h2></center>
<center><h3>(for noobs to both the ESP8266 and Micropython)</h3></center>
<form>
LED0:
<button name="LED" value="ON0" type="submit">LED ON</button>
<button name="LED" value="OFF0" type="submit">LED OFF</button><br><br>
LED2:
<button name="LED" value="ON2" type="submit">LED ON</button>
<button name="LED" value="OFF2" type="submit">LED OFF</button>
</form>
<!DOCTYPE html>
<html>
<form>
  <fieldset>
    <legend>Wifi Configuration</legend>
    <input type="text"     name="ssid"     value="%s" placeholder="SSID" />
    <input type="password" name="pw"       value="%s" placeholder="Password" />
    <input type="submit"   name="savewifi" value="SAVE" />
  </fieldset>
</form>
<form>
  <fieldset>
    <legend>Departures</legend>
    Number of displays:
    <input type="number" name="numdisp" min="0" max="8" value="1">
    <input type="submit" name="savenum" value="Update" />
    <table>
      <tr>
        <td></td>
        <td>Station</td>
        <td></td>
        <td></td>
        <td>Direction</td>
        <td></td>
        <td></td>
      </tr>
      <tr>
        <td>1</td>
        <td><input type="text"   name="sname"  placeholder="Station name" /></td>
        <td><input type="submit" name="getsid" value="Get ID" /></td>
        <td><input type="text"   name="sid"    placeholder="Station ID"/></td>
        <td><input type="text"   name="dname"  placeholder="Direction name" /></td>
        <td><input type="submit" name="getdid" value="Get ID" /></td>
        <td><input type="text"   name="did"    placeholder="Direction ID"/></td>
      </tr>
    </table>
    <input type="submit" name="savedep" value="SAVE" />
  </fieldset>
</form>
</html>
"""

#Setup PINS
LED0 = machine.Pin(0, machine.Pin.OUT)
LED2 = machine.Pin(2, machine.Pin.OUT)

#Setup Socket WebServer
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)
while True:
    conn, addr = s.accept()
    print("Got a connection from %s" % str(addr))
    request = conn.recv(1024)
    # print("Content = %s" % str(request))
    request = str(request)

    get = request.split("?")[1].split(" ")[0]

    print("")
    print("")
    print(get)
    allitems = get.split("&")
    items = {}
    items["ssid"] = "deault ssid"
    items["pw"] = "deault pw"
    for i in allitems:
        k, v = i.split("=")
        items[k] = v

    print(items)
    print("")
    print("")

    LEDON0 = request.find('/?LED=ON0')
    LEDOFF0 = request.find('/?LED=OFF0')
    LEDON2 = request.find('/?LED=ON2')
    LEDOFF2 = request.find('/?LED=OFF2')
    #print("Data: " + str(LEDON0))
    #print("Data2: " + str(LEDOFF0))
    if LEDON0 == 6:
        # print('TURN LED0 ON')
        LED0.low()
    if LEDOFF0 == 6:
        # print('TURN LED0 OFF')
        LED0.high()
    if LEDON2 == 6:
        # print('TURN LED2 ON')
        LED2.low()
    if LEDOFF2 == 6:
        # print('TURN LED2 OFF')
        LED2.high()
    response = html % (items["ssid"], items["pw"])
    conn.send(response)
    conn.close()
