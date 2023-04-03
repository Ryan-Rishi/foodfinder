import os
import googlemaps
from datetime import datetime
import numpy as np
import pandas as pd
import pgeocode
import requests
import json
import time

key = os.getenv("googleMapsAPI")
gmaps = googlemaps.Client(key)

# Gets the latitude and longitude of the zip code provided
def getLocation(zip):
    country = pgeocode.Nominatim('us')
    geoLoc = country.query_postal_code(zip)
    latitude = str(geoLoc.latitude)
    longitude = str(geoLoc.longitude)
    return str(latitude) + ',' + str(longitude)

# Returns a list of restaurants with a desired vicinty(Max 60)
def findRestaurants(radius=1000, zip = '30308'):
    coord = getLocation(zip)
    place_type = 'restaurant'
    # Define the keyword to search for (optional)
    keyword = 'food'

    # Make the Places API request
    places_result = gmaps.places_nearby(
        location=coord,
        radius=radius,
        type=place_type,
        keyword=keyword,
    )

    # Initialize a list to store the nearby restaurants
    nearby_restaurants = []

    # Loop through the results and add the name, address, and rating of each nearby restaurant to the list
    for place in places_result['results']:
        restaurant = {
            'name': place['name'],
            'address': place['vicinity'],
            'rating': place.get('rating', 'N/A')
        }
        nearby_restaurants.append(restaurant)
    
    while 'next_page_token' in places_result:
        time.sleep(1.5)
        page_token = places_result['next_page_token']
        places_result = gmaps.places_nearby(
            location=coord,
            radius=radius,
            type=place_type,
            keyword=keyword,
            page_token=page_token
        )
        
    # Loop through the next 20 results and add them to the list
        for place in places_result['results']:
            restaurant = {
                'name': place['name'],
                'address': place['vicinity'],
                'rating': place.get('rating', 'N/A')
            }
            nearby_restaurants.append(restaurant)
    # Pause for a second to allow the server to process the request

    # Print the list of nearby restaurants with their names, addresses, and ratings
    for restaurant in nearby_restaurants:
        print(restaurant['name'], restaurant['address'], restaurant['rating'])

if __name__ == "__main__":
    findRestaurants()
