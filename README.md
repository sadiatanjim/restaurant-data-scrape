# Scraping Restaurant Data using Google Places API

The Goal of this Project is to collect data from restaurants in Bangladesh using the Google Places API. 

The following data is collected for each restaurant:
- Name
- Place_id (Unique identifier to Google Maps)
- Location (Latitude & Longitude)
- Rating (on a scale of 5)
- No. of Reviews/Ratings
- Price Level ($/$$/$$$/$$$$)

If a data point is not available i.e. rating/reviews/price level, it is replaced with 'N/A'

# Project Organization: 

The different steps of the project are organized into a few different notebooks: 

1. data_scraping_places_API
2. generate_data_points
3. 
4. 
5. 

## Data Scraping using Places API

Data Scraping is performed using the Google Places API. We use the `nearby search` request of the Google Places API.

- We first try to collect restaurant data around a random point in Dhaka, Bangladesh using an API call
- The response is processed to extract relevant Data as a Python Dictionary with the function `get_loc_data()`
- Multiple pages of response can be extracted using the `next_page_token` in the function `get_nearby_locs()`
- The optimum radius of search in Dhaka was determined to be 150 meters. 

## Generate Data Points/Search Bubbles

With the optimal search radius of 150 meters, we can define search bubbles throughout geographic co-ordinates.

- A uniform grid of search bubbles are visualized with folium
- A more efficient hexagonal grid is realized

Before demonstrating on the whole country, we would like generate data points/search bubbles for Dhaka first. 

Geometric boundaries are usually defined in GeoJSON files. The GeoJSON file for Dhaka is collected from the following Link: [dhaka.geojson](https://gist.github.com/EmranAhmed/e1f1da00b6677aed023a) 

- The geojson file is processed
- An overlapping grid of data points/search bubbbles is generated for the search
- The search grid is visualized
- We write the function `get_all_points()` which takes a geographic polygon as input and returns a list of search co-ordinates within the bounds of the polygon