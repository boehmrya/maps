

import json

filename = 'metroArea_with_data.json'

with open(filename, 'r') as handle:
    parsed = json.load(handle)

dotMapDataFile = open("metroArea_with_data_pretty.json", "w")
dotMapDataFile.write(json.dumps(parsed, indent=4, sort_keys=True))
