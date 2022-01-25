import geopandas
from utils import get_all_points, get_nearby_locs
from tqdm import tqdm
import pandas as pd
import os

radius = 150
loc_type = 'restaurant'
api_key = 'API_KEY_GOES_HERE'

bd_geojson_path = 'PATH_TO_GEOJSON_FILE'
bd_geo = geopandas.read_file(bd_geojson_path)

csv_folder = 'PATH_TO_STORE_CSV_FILES'

idx = 0
n = len(bd_geo)

# Collecting Data using Google Places API

for index, row in bd_geo.iterrows():
    idx += 1
    id = row['id']
    sub_district = row['NAME_4']
    print('Processing: %s (%d/%d)'%(sub_district, idx, n))

    polygon = row['geometry']               # Extract Polygon for Subdistrict
    points = get_all_points(polygon)        # Generate Search Points

    data = []       # List to hold extracted data from nearby locations

    for lat, lng in tqdm(points):
        loc_data = get_nearby_locs(
            lat, lng, radius, loc_type, api_key, verbose = False)
        data.extend(loc_data)        

    # Create dataframe for sub-district, drop duplicates
    df = pd.DataFrame(data)
    df.sort_values("place_id", inplace=True)
    df.drop_duplicates(subset="place_id", keep=False, inplace=True)

    # Store dataframe as csv file
    # Encoding UTF-16 used to store Bangla Chars
    csv_savepath = os.path.join(csv_folder, id + '.csv')
    df.to_csv(csv_savepath, index=False, encoding = 'utf-16')

# Combining All Data

dfs = []

for index, row in bd_geo.iterrows():
    id = row['id']
    csv_path = os.path.join(csv_folder, id + '.csv')
    df = pd.read_csv(csv_path, encoding = "utf-16")
    dfs.append(df)

df_merged = pd.concat(dfs)

# Dropping Duplicates
df_merged.sort_values("place_id", inplace=True)
df_merged.drop_duplicates(subset="place_id", keep=False, inplace=True)

# Saving the merged DataFrame

merge_csv_path = os.path.join(csv_folder, 'results_merged.csv')
df_merged.to_csv(merge_csv_path, index=False, encoding = 'utf-16')