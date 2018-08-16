

import json

filename = 'us-states.json'

with open(filename, 'r') as handle:
    parsed = json.load(handle)

print json.dumps(parsed, indent=4, sort_keys=True)
