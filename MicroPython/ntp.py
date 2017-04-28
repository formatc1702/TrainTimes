import usocket as socket
import ustruct as struct
import utime as time

def get_time():
    #NTP_DELTA = 3155673600 - 1 * 60 * 60 # Adjust for CET
    NTP_DELTA = 3155673600 - 2 * 60 * 60 # Adjust for CEST... TODO: Make timezones smarter
    host = "pool.ntp.org"
    NTP_QUERY = bytearray(48)
    NTP_QUERY[0] = 0x1b
    addr = socket.getaddrinfo(host, 123)[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(1)
    res = s.sendto(NTP_QUERY, addr)
    msg = s.recv(48)
    s.close()
    val = struct.unpack("!I", msg[40:44])[0]
    return val - NTP_DELTA
