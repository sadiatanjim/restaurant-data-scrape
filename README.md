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
2. 
3. 
4. 
5. 

## Data Scraping using Places API

Data Scraping is performed using the Google Places API. We use the `nearby search` request of the Google Places API.

- We first try to collect restaurant data around a random point in Dhaka, Bangladesh using an API call
- The response is processed to extract relevant Data as a Python Dictionary
- Multiple pages of response can be extracted using the `next_page_token`
- The optimum radius of search in Dhaka was determined to be 150 meters. 


