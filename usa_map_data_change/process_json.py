

import json
import csv
import requests

# build dict with state to abbreviation translation
stateDict = {}
stateAbbrevDict = {}
with open('states.csv', 'rb') as csvfile:
    states = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in states:
        state = row[0][1:-1]
        abbrev = row[1][1:-1]
        stateDict[state] = abbrev
        stateAbbrevDict[abbrev] = state


# build dict with cities, states, and coordinates
metroCoordinates = {}
with open('cities_coordinates.json', 'r') as handle:
    parsed = json.load(handle)
    for item in parsed:
        city = item['fields']['city']
        stateFull = item['fields']['state']
        stateAbbrev = stateDict[stateFull]
        coordinates = item['geometry']['coordinates']
        # build dictionary
        key = city + ',' + stateAbbrev
        metroCoordinates[key] = {}
        metroCoordinates[key]['state'] = stateAbbrev
        metroCoordinates[key]['coordinates'] = coordinates


# output metro data to file
outputFile = open("output.json", "w")
outputFile.write(json.dumps(metroCoordinates, indent=4, sort_keys=True))


leftOvers = []
with open('dotMapData_v4.json', 'r') as handle:
    dotMapData = json.load(handle)
    for item in dotMapData['features']:
        name = item['properties']['NAME']
        if "-" in name:
            names = name.split('-')
            name = names[0]
        state = item['properties']['state']

        # adjust coordinates for each city
        coordsChanged = 0
        for key, value in metroCoordinates.iteritems():
            parts = key.split(',')
            cityName = parts[0]
            stateName = parts[1]
            if cityName in name:
                if stateName in state:
                    item['geometry']['coordinates'] = value['coordinates']
                    coordsChanged += 1

        if coordsChanged == 0:
            nameParts = name.split(',')
            cityOnly = nameParts[0]
            # test all possible states, quit after first success
            if "-" in state:
                states = state.split("-")
            else:
                states = [state]
            success = 0
            for theState in states:
                # quit if request comes back positive
                if success == 1:
                    break;
                else:
                    # convert to full state name
                    fullState = stateAbbrevDict[theState]
                    payload = {'city': cityOnly, 'state': fullState, 'country': 'USA', 'format': 'json'}
                    r = requests.get('https://nominatim.openstreetmap.org/search?', params=payload)
                    location = json.loads(r.content)
                if location != []:
                    lon = location[0]['lon']
                    lat = location[0]['lat']
                    item['geometry']['coordinates'] = [lon, lat]
                    success = 1
                else:
                    print cityOnly + ", " + fullState
                    leftOvers.append(name)
    print leftOvers


'''
# output metro data to file
outputFile = open("dotMapData_output.json", "w")
outputFile.write(json.dumps(dotMapData, indent=4, sort_keys=True))
'''

# output metro data to file
with open('dotMapData_output.json', 'w') as fp:
    json.dump(dotMapData, fp)
