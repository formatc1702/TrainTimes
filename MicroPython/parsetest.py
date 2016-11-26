from datetime import datetime
import urllib2

from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

displays = [
    ['Strassmannstr',
        ['Friedrich-Ludwig-Jahn-Sportpark', 'S+U Hauptbahnhof'],
        ['S+U Warschauer Str.']]
    ,
    ['S+Landsberger+Allee+%28Berlin%29',
        ['Ringbahn S 42'],
        ['Ringbahn S 41'],
        ['S Blankenburg (Berlin)','S+U Pankow (Berlin)','S Birkenwerder Bhf'],
        ['S Flughafen Berlin-Sch&#246;nefeld Bhf','Sch&#246;neweide','S Gr&#252;nau (Berlin)']]
    ,
    ['Bersarinplatz',
        ['Lichtenberg'],
        ['Sch&#246;neweide']]
    ]

results = [[[],[]],[[],[],[],[]],[[],[]]]

# print results

# station -> direction -> destination

for sta_index, station in enumerate(displays):
    url = 'http://mobil.bvg.de/Fahrinfo/bin/stboard.bin/dox?input=' + station[0] + '&start=Suchen&boardType=depRT'
    # print station[0]
    # print url

    directions = station[1:]

    response = urllib2.urlopen(url)
    # response = ['Woanders','S+U Warschauer Str.','Sonstwohin']


    for line in response: # where is the actual tram going?
        if line.startswith('Date:'):
            date_str = line[6:-1]
            print(date_str)                     # Sat, 26 Nov 2016 20:23:09 GMT
            date_obj = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %Z')
            print(date_obj.hour)
            print(date_obj.minute)
            print(date_obj.second)
        else:
            for dir_index, direction in enumerate(directions): # iterate through all directions tram can go at one station
                for destination_want in direction: # iterate through all destinations in that direction
                    if destination_want in line: # is the tram going where we want it to?
                        # print str(dir_index) + '...' + line.rstrip() + '...' + destination_want
                        response.readline()
                        response.readline()
                        response.readline()
                        # print response.readline()
                        results[sta_index][dir_index] += [strip_tags(response.readline()).rstrip()]
                continue
                # print destination_want
                # if destination_want in destination_is:
                #     print 'match!'

        # for direction in station[1:]:
        #     print '  ', direction

for idx_station, station in enumerate(results):
    print displays[idx_station][0]
    for direction in station:
        print direction





# urllib2.urlopen().read()
#
#
# with open('/Users/daniel/Documents/Development/1_Projects/TrainTimes/MicroPython/testfile/httprequest.txt','r') as f:
#     for line in f:
#         if line.startswith('Date:'):
#             date_str = line[6:-1]
#             print(date_str)                     # Sat, 26 Nov 2016 20:23:09 GMT
#             date_obj = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %Z')
#             print(date_obj.hour)
#             print(date_obj.minute)
#             print(date_obj.second)
#         # else:
#         #     print('no')
