from google.cloud import bigquery as bq
import pandas as pd
import gcsfs
import json
import functions_framework

@functions_framework.http
def bucket_geojson_to_bq(request):
   """HTTP Cloud Function.
   Args:
       request (flask.Request): The request object.
       <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
   Returns:
       The response text, or any set of values that can be turned into a
       Response object using `make_response`
       <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
   """
   request_json = request.get_json(silent=True)
   request_args = request.args    
   bigquery_client = bq.Client()                                                                           # Define a Bigquery client object
   if request_json and 'PROJECT' in request_json:
       name = request_json['PROJECT']
       gcs_file_system  = gcsfs.GCSFileSystem(project=request_json['PROJECT'])  # Define the file system of your Google Cloud project
       with gcs_file_system.open(f"gs://{request_json['BUCKET']}/{request_json['PATH_TO_FILE']}") as ifp:
        features = json.load(ifp)['features']
        table_id = f"{request_json['DATASET']}.{request_json['TABLE']}"
        data = []
        for obj in features:
            props = obj['properties']                                      # a dictionary
            props['geometry'] = json.dumps(obj['geometry'])                # make the geometry a string
            data.append(props)
        df = pd.DataFrame(data)
        job = bigquery_client.load_table_from_dataframe(df, table_id)                               # Make an API request.
        job.result() 
   elif request_args and 'PROJECT' in request_args:
       name = request_args['PROJECT']
   else:
       name = 'World'
   return f"The geojson file gs://{request_json['BUCKET']}/{request_json['PATH_TO_FILE']} has been pushed to Bigquery correctly as {request_json['PROJECT']}.{request_json['DATASET']}.{request_json['TABLE']}"
