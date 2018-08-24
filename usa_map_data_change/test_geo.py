
import requests
import json

payload = {'city': 'Greenfield Town', 'state': 'Massachusetts', 'country': 'USA', 'format': 'json'}
r = requests.get('https://nominatim.openstreetmap.org/search?', params=payload)

location = json.loads(r.content)
lon = location[0]['lon']
lat = location[0]['lat']
print [lon, lat]
