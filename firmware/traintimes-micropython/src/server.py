import socket
import machine

import wifi

w = wifi.WiFi()

#Setup Socket WebServer
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)
while True:
    conn, addr = s.accept()
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    request = str(request)
    # print(request)

    # extract GET parameters
    # get everything after the '?'
    if '?' in request:
        get = request.split('?')[1].split(' ')[0]
        # extract individual key=value pairs
        all_params = get.split('&')
        params = {}
        print('Got these parameters:')
        for i in all_params:
            k, v = i.split('=')
            params[k] = v
            print(f'{k}: {v}')

        # do stuff based on parameters

        # update wifi credentials
        if 'savewifi' in params:
            print('Changing the wifi credentials')
            print(f'New SSID: {params['ssid']}')
            print(f'New PW:   {params['pw']}')
            with open('wificonfig.txt','w') as f:
                f.write(f'{params['ssid']}\n')
                f.write(f'{params['pw']}\n')

    else:
        params = {}
        print('Got no parameters')

    # retrieve wifi credentials
    try:
        with open('wificonfig.txt','r') as f:
            real_ssid = f.readline().strip()
            real_pw   = f.readline().strip()
        print('Got these credentials from file:')
        print(f'{real_ssid} : {real_pw}')
    except:
        print('Error reading wifi config file')
        real_ssid = ''
        real_pw   = ''

    # initialize placeholders
    replacements = {
                    '$SSID': real_ssid,
                    '$PW':   real_pw
                   }

    # serve file filling placeholders
    with open('index.html','r') as f:
        while True:
            line = f.readline()
            if line:
                for old, new in replacements.items():
                    if old in line:
                        line = line.replace(old, new)
                        print(f'Replaced {old} with {new}')

                conn.send(line)
            else:
                break

    conn.close()
