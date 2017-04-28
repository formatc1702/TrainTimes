import urequests

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
        print(r)
        j = urequests.get(r).json()
        
        dates = []
        times = []
        for departure in j["Departure"]:
            if "rtTime" in departure:
                dates.append(departure["rtDate"])
                times.append(departure["rtTime"])
                print("REAL TIME")
            else:
                dates.append(departure["date"])
                times.append(departure["time"])
                print ("NOT!!!")
        return dates, times
