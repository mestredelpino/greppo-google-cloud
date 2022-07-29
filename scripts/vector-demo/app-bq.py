from greppo import app
import google.cloud.bigquery as bq
import os

gcp_project      = os.environ["PROJECT"]
dataset          = os.environ["DATASET"]

print(dataset)
print(gcp_project)

bigquery_client = bq.Client()

#
# Following function works for lines and points
def get_geodataframe(table,columns):
    sql_query = f"""
        SELECT ST_GeogFrom(geometry) as geometry, {columns}
        FROM {table}
    """
    geodataframe = bigquery_client.query(sql_query).to_geodataframe()
    return geodataframe


cities_df = get_geodataframe(f"{gcp_project}.{dataset}.cities","COUNTRY,NAME")
# roads_df = get_geodataframe(f"{gcp_project}.{dataset}.roads","COUNTRY,name")
# regions_df = get_geodataframe(f"{gcp_project}.{dataset}.regions","reg_name,reg_istat_code")

print(cities_df)

app.display(name='title', value='Vector demo')
app.display(name='description',
            value='A Greppo demo app for vector data using GeoJSON data.')

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


# app.vector_layer(
#     data=regions_df,
#     name="Regions of Italy",
#     description="Polygons showing the boundaries of regions of Italy.",
#     style={"fillColor": "#4daf4a"},
# )

# app.vector_layer(
#     data=roads_df,
#     name="Highways in Italy",
#     description="Lines showing the major highways in Italy.",
#     style={"color": "#377eb8"},
# )

app.vector_layer(
    data=cities_df,
    name="Cities of Italy",
    description="Points showing the cities in Italy.",
    style={"color": "#e41a1c"},
    visible=True,
)

text_1 = """
## About the web-app

The dashboard shows the boundaries of the regions of Italy as polygons, the 
major arterial higways as lines and the major cities of each region as points.
"""

app.display(name='text-1', value=text_1)

app.display(name='text-2',
            value='The following displays the count of polygons, lines and points as a barchart.')

# app.bar_chart(name='Geometry count', description='A bar-cart showing the count of each geometry-type in the datasets.',
#               x=['polygons', 'lines', 'points'], y=[len(regions_df), len(roads_df), len(cities_df)], color='#984ea3')


