from datetime import datetime
import urllib2

displays = [
    ['Strassmannstr',
        ['Friedrich-Ludwig-Jahn Sportpark', 'S+U Hauptbahnhof'],
        ['S+U Warschauer Str.']],
    ['S+Landsberger+Allee+%28Berlin%29',
        ['Ring S41'],
        ['Ring S42'],
        ['Pankow', 'Waidmannslust'],
        ['Grunau', 'Zeuthen']],
    ['Bersarinplatz',
        ['Lichtenberg'],
        ['S Schoneweide']]
    ]

# station -> direction -> destination

for station in displays:
    url = 'http://mobil.bvg.de/Fahrinfo/bin/stboard.bin/dox?input=' + station[0] + '&start=Suchen&boardType=depRT'
    print station[0]
    print url

    directions = station[1:]

    # response = urllib2.urlopen(url)
    response = ['Woanders','S+U Warschauer Str.','Sonstwohin']


    for destination_is in response: # where is the actual tram going?
        for direction in directions: # iterate through all directions tram can go at one station
            for destination_want in direction: # iterate through all destinations in that direction
                if destination_want in destination_is: # is the tram going where we want it to?
                    print 'match!'
            continue
            # print destination_want
            # if destination_want in destination_is:
            #     print 'match!'

    # for direction in station[1:]:
    #     print '  ', direction







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
