import pandas as pd
import json
import random
import requests
import numpy as np
import re
import geopandas as gpd
import urllib.parse
import os
from dotenv import load_dotenv

load_dotenv()

# Loading dataset
df_addresses = pd.read_csv('assignment7_slim_hospital_addresses.csv')
df_coordinates = pd.read_csv('assignment7_slim_hospital_coordinates.csv')

# Randomly selecting 100 rows from each dataset
random_addresses = random.sample(list(addresses_df['address']), 100)
random_coordinates = coordinates_df.sample(100)

# Geocoding
google_response = []

for address_here in random_addresses: 
    api_key =  os.getenv("GOOGLE_MAPS_API")

    search = 'https://maps.googleapis.com/maps/api/geocode/json?address='

    location_raw = address
    location_clean = urllib.parse.quote(location_raw)

    url_request_part1 = search + location_clean + '&key=' + api_key
    url_request_part1
    
    response = requests.get(url_request)
    response_dictionary = response.json()

    if response_dictionary['status'] == 'OK':
        lat_long = response_dictionary['results'][0]['geometry']['location']
        lat_response = lat_long['lat']
        lng_response = lat_long['lng']

        final = {'address': address, 'lat': lat_response, 'lon': lng_response}
        google_response.append(final)
        print(f'SUCCESSFUL geocoding for {address}')
    else:
        print(f'UNSUCCESSFUL for {address}')

df_geocoding = pd.DataFrame(google_response)

# Reverse Geocoding
reverse_geocode_url = 'https://maps.googleapis.com/maps/api/geocode/json?latlng='

google_response_reverse = []

for index, row in random_coordinates.iterrows():
    latitude = row['latitude']
    longitude = row['longitude']

    reverse_url_request = reverse_geocode_url + latitude + ',' + longitude + '&key=' + api_key
    reverse_url_request

    reverse_response = requests.get(reverse_url_request)
    reverse_response_dictionary = reverse_response.json()

    if reverse_response_dictionary['status'] == 'OK':
        reverse_address = reverse_response_dictionary['results'][0]['formatted_address']
        final_reverse = {'lat': latitude, 'lon': longitude, 'address': reverse_address}
        google_response_reverse.append(final_reverse)
        print(f'SUCCESSFUL reverse geocoding for ({latitude}, {longitude})')
    else:
        print(f'UNSUCCESSFUL reverse geocoding for ({latitude}, {longitude})')

df_reverse = pd.DataFrame(google_response_reverse)

# Function 
def geocode(address_here): 
    api_key =  os.getenv("GOOGLE_MAPS_API")

    search = 'https://maps.googleapis.com/maps/api/geocode/json?address='

    location_raw = address_here
    location_clean = urllib.parse.quote(location_raw)

    url_request_part1 = search + location_clean + '&key=' + api_key
    
    response = requests.get(url_request)
    response_dictionary = response.json()

    if response_dictionary['status'] == 'OK':
        lat_long = response_dictionary['results'][0]['geometry']['location']
        lat_response = lat_long['lat']
        lng_response = lat_long['lng']

        final = {'address': address_here, 'lat': lat_response, 'lon': lng_response}
        return final
    else:
        return None