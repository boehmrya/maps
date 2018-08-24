

import json

filename = 'tl_2017_us_uac10.json'

with open(filename, 'r') as handle:
    parsed = json.load(handle)

coordsDataFile = open("geo_coords_pretty.json", "w")
coordsDataFile.write(json.dumps(parsed, indent=4, sort_keys=True))
