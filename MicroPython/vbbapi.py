import usocket as socket
import http
import ujson as json

class API:
    def __init__(self):
        self.base_url = "http://demo.hafas.de/openapi/vbb-proxy"

        f = open("apikey.txt","r")
        self.api_key =  f.readline().rstrip()
        f.close()

        self.tail = "format=json&accessId={}".format(self.api_key)

    def get_station_id(self, station_name):
        src = http.get("{}/location.name?input={}&{}".format(self.base_url, station_name, self.tail))
        while True:
            line = src.readline().decode("utf-8")
            if line:
                if line[0] == "{":
                    j = json.loads(line)
                    return j["stopLocationOrCoordLocation"][0]["StopLocation"]["extId"]
            else:
                break

    def get_departures(self, station_id, max_journeys=0, direction_id=""):
        if max_journeys > 0:
            p_journeys = "&maxJourneys={}".format(max_journeys)
        else:
            p_journeys = ""
        if direction_id != "":
            p_dir = "&direction={}".format(direction_id)
        else:
            p_dir = ""
        src = http.get("{}/departureBoard?extId={}{}{}&{}".format(self.base_url, station_id, p_dir, p_journeys, self.tail))
        while True:
            line = src.readline().decode("utf-8")
            if line:
                if line[0] == "{":
                    j = json.loads(line)
                    return j
            else:
                break
