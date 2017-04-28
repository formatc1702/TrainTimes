import urequests
import utime as time

class API:
    def __init__(self):
        self.base_url = "http://demo.hafas.de/openapi/vbb-proxy/"

        f = open("apikey.txt","r")
        self.api_key =  f.readline().rstrip()
        f.close()

        self.tail = "format=json&accessId={}".format(self.api_key)

    def create_request(self, command):
        return "{}{}&{}".format(self.base_url, command, self.tail)

    def get_station_id(self, station_name, verbose=False):
        r = self.create_request("location.name?input={}".format(station_name))
        if verbose:
            print(r)
        j = urequests.get(r).json()
        return j["stopLocationOrCoordLocation"][0]["StopLocation"]["extId"]

    def get_departures(self, station_id, max_journeys=0, direction_id="", verbose=False):
        if max_journeys > 0:
            p_journeys = "&maxJourneys={}".format(max_journeys)
        else:
            p_journeys = ""
        if direction_id != "":
            p_dir = "&direction={}".format(direction_id)
        else:
            p_dir = ""

        r = self.create_request("departureBoard?extId={}{}{}".format(station_id, p_dir, p_journeys))
        if verbose:
            print(r)
        j = urequests.get(r).json()

        times = []
        for departure in j["Departure"]:
            if "rtTime" in departure:
                datestring = departure["rtDate"]
                timestring = departure["rtTime"]
                if verbose:
                    print("REAL TIME")
            else:
                datestring = departure["date"]
                timestring = departure["time"]
                if verbose:
                    print ("NOT!!!")

            year, month,  day    = [int(i) for i in datestring.split('-')]
            hour, minute, second = [int(i) for i in timestring.split(':')]
            u = time.mktime([year, month, day, hour, minute, second, 0, 0])
            times.append(u)
        return times
