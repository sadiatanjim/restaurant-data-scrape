import itertools
import numpy as np
import folium
from shapely.geometry import Point
import requests
import json
import time

def get_center(bounds):
    '''
    get center of provided bounds
    '''
    lng_min, lat_min, lng_max, lat_max = bounds
    lat = (lat_min + lat_max)/2
    lng = (lng_min + lng_max)/2
    return lat, lng 

def get_all_points(polygon, step = 250, shift = 150):
    '''
    This function takes a shapely polygon as an input and returns a list of
    co-ordinates within the polygon
    Args:
    - step: horizontal,vertical step
    - shift: shift for every other point
    '''

    mtodeg = 1/111111       # 1m = 1/111111 deg (approx.)
    lng_min, lat_min, lng_max, lat_max = polygon.bounds


    lats_even = np.arange(start = lat_min, stop = lat_max, step = step*mtodeg)
    lats_odd = np.arange(start = lat_min + shift*mtodeg, stop = lat_max, step = step*mtodeg)

    lngs_even = np.arange(start = lng_min, stop = lng_max, step = 2*step*mtodeg)
    lngs_odd = np.arange(start = lng_min + step*mtodeg, stop = lng_max, step = 2*step*mtodeg)

    even_points = itertools.product(lats_even, lngs_even)
    odd_points = itertools.product(lats_odd, lngs_odd)

    valid_points = []

    for point in even_points:
        lat, lng = point
        point = Point(lng, lat)
        if(point.within(polygon)): valid_points.append([lat, lng])

    for point in odd_points:
        lat, lng = point
        point = Point(lng, lat)
        if(point.within(polygon)): valid_points.append([lat, lng])

    return valid_points

def draw_circle(map, latitude, longitude, radius):
    '''
    Draw circle onto a folium map
    '''
    folium.vector_layers.Circle(
        location=[latitude, longitude],
        radius=radius,
        color='#3186cc',
        fill=True,
        fill_color='#3186cc'        
    ).add_to(map)
    return map

def get_loc_data(
    data, extra_keys = ['rating', 'user_ratings_total', 'price_level']
):
    '''
    Function to get location data from a API Call result
    returns name, place_id, latitude & longitude
    also returns extra_keys appended as a python dictionary
    '''
    data_dict = {}
    data_dict['name'] = data['name']
    data_dict['place_id'] = data['place_id']
    data_dict['latitude'] = data['geometry']['location']['lat']
    data_dict['longitude'] = data['geometry']['location']['lng']

    for key in extra_keys:
        try:
            if key == 'price_level':
                # Prints $, $$, $$$, $$$$ for price levels 1, 2, 3, 4
                data_dict[key] = '$'*data[key]
            else:
                data_dict[key] = data[key]
        except:
            data_dict[key] = 'N/A'
    
    return data_dict

def get_nearby_locs(latitude, longitude, radius, loc_type, api_key, verbose = True):
    '''
    Calls the Google Places API to get a list of Nearby Locations
    Args: 
    - latitude
    - longitude
    - radius (in meters)
    - loc_type : type of location
    - api_key
    - verbose: Set the verbosity of the function
    '''
    responses = []      # Array for storing multiple responses

    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={},{}&radius={}&type={}&key={}".format(latitude, longitude, radius, loc_type, api_key)

    if verbose: print('Sending Request to Google Places API.')
    # Initial Query
    response = requests.request("GET", url, headers={}, data={})
    response_dict = json.loads(response.text)   # Convert to Dictionary
    responses.append(response_dict)

    while ('next_page_token' in response_dict.keys()):
        if verbose: print('Waiting for next page ...')
        time.sleep(2)       # Wait for 2 seconds for next page to load
        next_page_token = response_dict['next_page_token']
        url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?pagetoken={}&key={}".format(next_page_token, api_key)
        response = requests.request("GET", url, headers={}, data={})
        response_dict = json.loads(response.text)
        responses.append(response_dict)

    if verbose: print('Received all responses. Scraping responses ...', end = '\t')
    
    data_dict = []      # Array of dictionaries containing data

    for response in responses:
        for result in response['results']:
            data_dict.append(get_loc_data(result))

    if verbose: print('Complete!')

    return data_dict

