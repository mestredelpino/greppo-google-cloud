import geojson
import json

import pandas
import pandas_gbq
import geopandas as gpd

from google.cloud import bigquery as bq
import gcsfs
import os


gcp_project      = os.environ["PROJECT"]
dataset          = os.environ["DATASET"]
table            = os.environ["TABLE"]
geojson_file_url = os.environ["GEOJSON_FILE_URL"]

# Define the file system of your Google Cloud project
gcs_file_system  = gcsfs.GCSFileSystem(project=gcp_project)

# Open 
# with gcs_file_system.open(geojson_file_url) as geojson_file:
#   json_file = json.load(geojson_file)

# geodataframe = gpd.GeoDataFrame.from_features(json_file["features"])

bigquery_client = bq.Client()






# # This example uses a table containing a column named "geo" with the
# # GEOGRAPHY data type.
# table_id = f"{gcp_project}.{dataset}.{table}"

# # Use the python-geojson library to generate GeoJSON of a line from LAX to
# # JFK airports. Alternatively, you may define GeoJSON data directly, but it
# # must be converted to a string before loading it into BigQuery.
# my_geography = geojson.LineString([(-118.4085, 33.9416), (-73.7781, 40.6413)])
# rows = [
#     # Convert GeoJSON data into a string.
#     {"geometry": geojson.dumps(my_geography)}
# ]

# #  table already exists and has a column
# # named "geo" with data type GEOGRAPHY.
# errors = bigquery_client.insert_rows_json(table_id, rows)
# if errors:
#     raise RuntimeError(f"row insert failed: {errors}")
# else:
#     print(f"wrote 1 row to {table_id}")


#########

with gcs_file_system.open(geojson_file_url) as ifp:
  with open('to_load.json', 'w') as ofp:
    features = json.load(ifp)['features']
    # new-line-separated JSON
    schema = None
    for obj in features:
        props = obj['properties']  # a dictionary
        props['geometry'] = json.dumps(obj['geometry'])  # make the geometry a string
        # props['longitude'] = 
        # props['latitude']
        json.dump(props, fp=ofp)
        print('', file=ofp) # newline
        if schema is None:
            schema = []
            for key, value in props.items():
                if key == 'geometry':
                    schema.append('geometry:GEOGRAPHY')
                elif isinstance(value, str):
                    schema.append(key)
                else:
                    schema.append('{}:{}'.format(key,
                       'int64' if isinstance(value, int) else 'float64'))
            schema = ','.join(schema)
    print('Schema: ', schema)


# Then run this on bash:
# bq load --source_format NEWLINE_DELIMITED_JSON --autodetect {dataset}.{table} to_load.json