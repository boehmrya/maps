from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="ryan")
location = geolocator.geocode('Hammond, LA', addressdetails=True)
print (location.latitude, location.longitude)
