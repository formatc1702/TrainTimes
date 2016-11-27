# displays = {
#     'Strassmannstr' : {
#         'North': ['Friedrich-Ludwig-Jahn Sportpark', 'S+U Hauptbahnhof'],
#         'South': ['Warschauer Str']},
#     'S Landsberger Allee': {
#         'Ring CCW': ['Ring S41'],
#         'Ring CW': ['Ring S42'],
#         'North': ['Pankow', 'Waidmannslust'],
#         'South': ['Grunau', 'Zeuthen']},
#     'Bersarinplatz': {
#         'North': ['Lichtenberg'],
#         'South' : ['S Schoneweide']}
#     }
#
displays = [
    ['Strassmannstr',
        ['Friedrich-Ludwig-Jahn Sportpark', 'S+U Hauptbahnhof'],
        ['Warschauer Str']],
    ['S Landsberger Allee',
        ['Ring S41'],
        ['Ring S42'],
        ['Pankow', 'Waidmannslust'],
        ['Grunau', 'Zeuthen']],
    ['Bersarinplatz',
        ['Lichtenberg'],
        ['S Schoneweide']]
    ]

test = ['Woanders','Warschauer Str','Sonstwohin']

for station in displays:
    print station[0]
    for direction in station[1:]:
        print '  ', direction
        for testitem in test:
            if direction == testitem:
                print 'match'
            else:
                print testitem
