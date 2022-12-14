from greppo import app
import google.cloud.bigquery as bq
import os

gcp_project      = os.environ["PROJECT"]
dataset          = os.environ["DATASET"]

bigquery_client = bq.Client()


# Following function works for lines and points
def get_geodataframe(table,columns):
    sql_query = f"""
        SELECT ST_GeogFrom(geometry) as geometry, {columns}
        FROM {table}
    """
    geodataframe = bigquery_client.query(sql_query).to_geodataframe()
    return geodataframe

def choose_feature(table,columns,feature_name):
    sql_query = f"""
        SELECT ST_GeogFrom(geometry) as geometry, {columns} FROM {table} WHERE reg_name = '{feature_name}'
    """
    geodataframe = bigquery_client.query(sql_query).to_geodataframe()
    return geodataframe

def point_in_polygon(columns,points_table_id,polygons_table_id,polygons_key,polygons_value):
    sql_query = f"""
        SELECT {columns} FROM {points_table_id} as points 
        JOIN {polygons_table_id} as polygons 
        ON ST_Within(ST_GeogFrom(points.geometry), ST_GeogFrom(polygons.geometry)) 
        WHERE polygons.{polygons_key} = '{polygons_value}'
    """
    geodataframe = bigquery_client.query(sql_query).to_geodataframe()
    return geodataframe


cities_df = get_geodataframe(f"{gcp_project}.{dataset}.cities","COUNTRY,NAME")
roads_df = get_geodataframe(f"{gcp_project}.{dataset}.roads","COUNTRY,name")
regions_df = get_geodataframe(f"{gcp_project}.{dataset}.regions","reg_name,reg_istat_code")


text_1 = """
## About the web-app

The dashboard shows the boundaries of the regions of Italy as polygons, the 
major arterial higways as lines and the major cities of each region as points.
"""

app.display(name='title', value='Vector demo')
app.display(name='description',
            value='A Greppo demo app for vector data using GeoJSON data.')

app.display(name='text-1', value=text_1)

app.base_layer(
    name="Open Street Map",
    visible=True,
    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
    subdomains=None,
    attribution='(C) OpenStreetMap contributors',
)

app.base_layer(
    provider="CartoDB Positron",
)


app.vector_layer(
    data=roads_df,
    name="Highways in Italy",
    description="Lines showing the major highways in Italy.",
    style={"color": "#377eb8"},
)

app.vector_layer(
    data=cities_df,
    name="Cities of Italy",
    description="Points showing the cities in Italy.",
    style={"color": "#e41a1c"},
    visible=True,
)


# Choose city
# for i in cities_df["NAME"]:
#     city_choice.append(i)

# chosen_city = app.select(name="Choose city", options=city_choice, default=city_choice[0])

# Choose region


region_choice = []

for i in regions_df["reg_name"]:
    region_choice.append(i)

chosen_region = app.select(name="Choose region", options=region_choice, default=region_choice[0])

regions_display = choose_feature(f"{gcp_project}.{dataset}.regions","reg_name,reg_istat_code",chosen_region)

cities_in_region = point_in_polygon("ST_GeogFrom(points.geometry), points.NAME, polygons.reg_name", f"{gcp_project}.{dataset}.cities",f"{gcp_project}.{dataset}.regions","reg_name",chosen_region)



app.vector_layer(
    data=regions_display,
    name="Regions of Italy",
    description="Polygons showing the boundaries of regions of Italy.",
    style={"fillColor": "#4daf4a"},
)


app.display(name='text-2',
            value='The following displays the count of polygons, lines and points as a barchart.')

app.bar_chart(name='City count', description='A bar-cart showing the count of each geometry-type in the datasets.',
              x=[f'Cities in the region {chosen_region}'], y=[len(cities_in_region["NAME"])], color='#984ea3')


