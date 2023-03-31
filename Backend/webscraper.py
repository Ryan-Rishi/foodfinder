import os
import googlemaps
from datetime import datetime
import numpy as np
import pandas as pd
import pgeocode

zip = "30308"

key = os.getenv("googleMapsAPI")
gmaps = googlemaps.Client(key)

country = pgeocode.Nominatim('us')
geoLoc = country.query_postal_code(zip)
latitude = str(geoLoc.latitude)
longitude = str(geoLoc.longitude)

url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location='+latitude+longitude+'&radius='+str(radius)+'&keyword='+str(keyword)+'&key='+str(api_key)
