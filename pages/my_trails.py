# my_trails.py

import dash
from dash import dcc, html, Input, Output, State, ClientsideFunction, callback, clientside_callback
import dash_leaflet as dl
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from dash import callback_context

import xml.etree.ElementTree as ET
from shapely.geometry import LineString, Point
import os
import pandas as pd
from geopy.distance import geodesic
import base64
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from math import *
import time
import requests

from database import get_session, Trails, Uploads

dash.register_page(__name__, title='WildStep My Trails')

clientside_callback(
    ClientsideFunction(namespace='clientside', function_name='trigger_gsap_animation'),
    Output('mytrail-dummy-output', 'children'),
    [Input('mytrail-dummy-input', 'children')]
)

clientside_callback(
    ClientsideFunction(namespace='clientside', function_name='scroll_to_map'),
    # Dummy output, we don't actually need to update anything in the layout
    Output('mytrail-dummy-output-2', 'children'),
    [Input('mytrail-search-dropdown', 'value')]
)

Session, connection = get_session()

df_trails = pd.read_sql('SELECT * FROM trails', con=connection)

external_stylesheets = [
    'https://fonts.googleapis.com/css?family=Poppins:300,400,500,600,700,800,900&display=swap',
    '/assets/style.css',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css',
    dbc.themes.MINTY
]

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'assets/lifeonland-418914-00a1094d16b6.json'


# def detect_labels(path):
#     """Detects labels in the file."""
#     from google.cloud import vision
#     client = vision.ImageAnnotatorClient()
#     # content = base64.b64decode(path)
#     image = vision.Image(content=path)
#     response = client.label_detection(image=image)
#     labels = response.label_annotations
#     if response.error.message:
#         raise Exception(
#             "{}\nFor more info on error messages, check: "
#             "https://cloud.google.com/apis/design/errors".format(response.error.message)
#         )
#     return labels

text = '''
Based on the image I am giving you, tell me three of the following things based on the main species identified in the image.
1. Vernacular name of the species
2. if it is endangered, vulnerable, critically endangered return “Endangered”. If it is venomous, poisonous or dangerous return “Dangerous”. If it is neither of the above return “Normal”
3. description of the species in under 1000 characters.
I want you to return each of the questions separated by “|”
An example:
Koala | Endangered | The Koala is a marsupial native to Australia. They primarily feed on eucalyptus leaves and are known for their distinctive large nose, fluffy ears, and thick fur. Habitat destruction and disease are significant threats to their population.
If no species is identified just respond with "None"
'''
def encode_image_to_base64(image_bytes):
    return base64.b64encode(image_bytes).decode('utf-8')
def detect_labels(image_bytes):
    api_key = "sk-proj-YBWxMoXBkkcVk2Qz1p3yT3BlbkFJdobay4XZHCDQE8BpSp5S "   
    # Encode the image content to base64
    image_base64 = encode_image_to_base64(image_bytes)
    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
    }
    # Send the image as part of a text message
    payload = {
        'model': "gpt-4-turbo",
        'messages': [
            {
                "role": "user",
                "content": [
                    {
                        'type': 'text',
                        'text':  text
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{image_base64}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    response_data = response.json()  
   
    if 'choices' in response_data and len(response_data['choices']) > 0:
        return response_data['choices'][0]['message']['content']
    else:
        return "None"


def get_unique_species(df):
    unique_values = set()
    for row in df['trail_species']:
        items = row.split(', ')
        unique_values.update(item.strip() for item in items)
    unique_species = [x.lower() for x in list(unique_values)]
    return unique_species


def gpx_to_points(gpx_path):
    tree = ET.parse(gpx_path)
    root = tree.getroot()
    namespaces = {'default': 'http://www.topografix.com/GPX/1/1'}
    route_points = [(float(pt.attrib['lat']), float(pt.attrib['lon']))
                    for pt in root.findall('.//default:trkpt', namespaces)]
    return LineString(route_points)


def load_trail_names():
    # df = pd.read_csv('data/50_trails.csv', encoding='utf-8')
    return [{'label': name, 'value': name} for name in df_trails['trail_name'].unique()]


def is_within_distance(point, trail_points, max_distance=500):
    return any(geodesic(point, trail_point).meters <= max_distance for trail_point in trail_points)


def b64_image(img):
    with open(img, 'rb') as f:
        image = f.read()
    return 'data:image/png;base64,' + base64.b64encode(image).decode('utf-8')


def db_img(blob):
    return 'data:image/png;base64,' + base64.b64encode(blob).decode('utf-8')

from math import log, tan, radians, cos, pi

def estimate_zoom(min_lat, max_lat, min_lon, max_lon, map_width_px=400, map_height_px=400):
    # Constants to adjust sensitivity of zoom calculation
    BASE_LAT_DIFF = 360 / (2 ** 12)  # Roughly the lat diff for zoom level 12
    BASE_LON_DIFF = 360 / (2 ** 12)  # Roughly the lon diff for zoom level 12

    # Latitude and Longitude Differences
    lat_diff = max(max_lat - min_lat, 0.0001)
    lon_diff = max(max_lon - min_lon, 0.0001)

    # Estimating zoom by comparing actual diff to base diff
    zoom_lat = log(BASE_LAT_DIFF / lat_diff) / log(2) + 12  # Adjust 12 according to your base zoom level
    zoom_lon = log(BASE_LON_DIFF / lon_diff) / log(2) + 12

    # Calculate suitable zoom level, ensuring it is within reasonable bounds
    estimated_zoom = min(zoom_lat, zoom_lon)
    estimated_zoom = max(min(estimated_zoom, 18), 5)  # Limit zoom levels to between 5 and 18

    return estimated_zoom

MAX_RETRIES = 3
RETRY_INTERVAL = 5 
def fetch_data(model):
    """Attempt to fetch data with retries for handling database connectivity issues."""
    session = Session()
    try:
        for attempt in range(MAX_RETRIES):
            try:
                data = session.query(model).all()
                return data
            except SQLAlchemyError as e:
                print(f"Attempt {attempt + 1}: Error fetching data - {e}")
                session.rollback()
                time.sleep(RETRY_INTERVAL)
    finally:
        session.close()
    return None


layout = dbc.Container(fluid=True, children=[

    dcc.Geolocation(id='geo'),
    html.Section(className='parallax', 
        children=[
        dbc.Row([
            dbc.Col([
                html.Img(src=b64_image('assets/all_trails_bg.png'), style={'z-index':'-1', 'opacity':'0.3', 'wdith':'150%', 'height':'auto'}),
                html.Img(src=b64_image('assets/alert.png'), style={'width':'25%', 'height':'auto', 'margin-left':'5%', 'margin-bottom':'5%'})
                ], width=3),
                dbc.Col([
                    html.Div([
                        html.P('Find species on your trail', style={'font-size': '3em', 'color': '#47483c', 'margin-left':'20%'}),
                        # html.H2('Be Alert.', id = 'text4',style={'font-size': '3em', 'color': '#F9F1E8', 'margin-bottom': '10px', 'margin-top': '-12%', 'margin-left':'50px', 'text-align':'center'}),
                        html.P(" "),
                        html.H4("Get real time updates on species found on your trail. Let's share interesting wildlife we find around Victoria", style={'margin-bottom': '10px', 'color': '#545646', 'text-align':'left', 'margin-left':'15%', 'padding':'5%'}),
                        # html.Img(src=b64_image('assets/element1.png'), id = 'alert', style={'width':'40%', 'height':'auto', 'margin-left':'100%', 'margin-top':'150%', 'z-index':'-1'}),
                        dcc.Dropdown(
                            id='mytrail-search-dropdown',
                            options=load_trail_names(),
                            searchable=True,
                            placeholder="Tell us the trail you're on...",
                            style={
                                'width': '70%',  # Use 100% to make it responsive within the column
                                'margin': '0 auto',  # Keep it centered
                                'borderRadius': '20px',
                                'fontFamily': '"Poppins", sans-serif',
                                'fontSize': '16px',
                                # 'padding': '20%',
                                'margin-left': '15%',
                                'borderWidth': '2px',
                                'borderColor': '#D9D9D9'
                            }
                        ),
                        dcc.Link(html.Button("Don't know which trail? Let us recommend one to you", n_clicks=0, style={'text-decoration': 'none', 'padding': '6px 15px', 'background': '#545646', 'color': '#F9F1E8', 'border-radius': '20px', 'margin-top':'30px', 'margin-left': '26%',}), 
                                 href="/explore-species", refresh=True),
            
                    ])
                ], width=9)
            ]),
    ]),
    html.Div(id='scroll-trigger', style={'display': 'none'}),
    html.Div(id='mytrail-dummy-input', style={'display': 'none'}),
    html.Div(id='mytrail-dummy-output', style={'display': 'none'}),
    html.Div(id='mytrail-dummy-output-2', style={'display': 'none'}),
    html.Div(
        dbc.Row([
                dbc.Col([
                    dbc.Row(justify="center", className="h-100 align-items-center", children=[
                        dbc.Col([
                            html.H4("See what other hikers have found on your trail",
                                    style={'color': '#F9F1E8', 'text-align': 'center'}),
                            html.P("   "),
                            html.P("Hover over each icon on the map to find interesting finds & species.",
                                   style={'color': '#F9F1E8', 'text-align': 'center'}),
                            html.P("   "),
                            # html.P("Please share your location before seeing real-time updates",
                            #        style={'color': '#545646', 'text-align': 'center'}),
                            html.Div(children=[
                                html.P("ⓘ Seems like you are too far from trail. If you still want to upload the image, tell us approximately where you found it?", style={'font-size':'0.9em', 'color':'#eae1d8', 'text-align': 'center'}),
                                dcc.Dropdown(
                                    id='section-search-dropdown',
                                    options=['Towards the beginning', 'Somewhere in the middle of the trail', 'Only at the end'],
                                    placeholder="Select the part of trail...",
                                    style={
                                        'width': '80%',  # Use 100% to make it responsive within the column
                                        'margin': '0 auto',  # Keep it centered
                                        'borderRadius': '20px',
                                        'fontFamily': '"Poppins", sans-serif',
                                        'fontSize': '16px',
                                        # 'padding': '20%',
                                        # 'margin-left': '15%',
                                        'borderWidth': '2px',
                                        'borderColor': '#D9D9D9'
                                    }
                                )
                            ], style={'display':'none'}, id='too-far-section'),
                            dcc.Loading(
                                id="loading-upload",
                                type="default",  # Or any other type you prefer
                                children=[
                                    dcc.Upload(
                                        id='upload-image',
                                        children=html.Div([html.I(className="fas fa-solid fa-upload"),
                                                           '   Found something interesting? Upload it!'], style={'margin-top': '10px'}),
                                        style={'display': 'block', 'width': '100%', 'height': '50px',
                                               'color': '#545646', 'backgroundColor': '#e8dfd4', 'lineHeight': '50px',
                                               'border': 'none', 'borderRadius': '20px', 'textAlign': 'center',
                                               'cursor': 'pointer', 'transition': 'all 0.2s ease-in-out', 'opacity': '0.6'},  # Initial style (disabled)
                                        accept='.png,.jpg,.jpeg,.heic',
                                        multiple=True
                                    ),
                                ]),
                            dbc.Tooltip("Please share your location/section & choose your trail to enable uploads.",
                                        target="upload-image",  # Match the id of dcc.Upload
                                        id="tooltip-upload",
                                        is_open=False,
                                        style={'display': 'block'}),
                            html.Div(id='upload-status', style={'margin-top': '30px', 'textAlign': 'center'})
                            # ])
                        ], width=10)  # Adjust width as needed for aesthetic preferences
                    ])
                ], width=9, lg=5, className="d-flex"),
                dbc.Col([
                    # dl.Map(
                    #     id='mytrail-map',
                    #     children=[dl.TileLayer(), dl.LayerGroup(id='mytrail-layer'), dl.LayerGroup(id='myimage-layer')],
                    #     style={'width': '100%', 'height': '640px', 'margin-top': '40px',
                    #            'margin-bottom': '40px', 'margin-left': '20px'},
                    #     center=(-37.8136, 144.9631),
                    #     zoom=12
                    # )
                    dl.Map(
                        id='mytrail-map',
                        children=[
                            dl.TileLayer(
                                # url='https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png',
                                # attribution='© OpenStreetMap contributors'
                                url = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}.png',
                                attribution = 'Tiles Courtesy of <a href="http://www.esri.com/software/arcgis/arcgisonline/maps/maps-and-map-layers" target="_blank">Esri</a>'
                            ),
                            dl.LayerGroup(id='mytrail-layer'),
                            dcc.Loading(  # Wrap the layer or component being updated with the loading indicator
                                id="loading-layer",
                                type="default",
                                children=dl.LayerGroup(id='myimage-layer')
                            )
                        ],
                        style={'width': 'auto', 'height': '500px', 'margin-top': '40px',
                               'margin-bottom': '40px', 'margin-right': '40px', 'borderRadius':'30px'},
                        center=(-37.8136, 144.9631),
                        zoom=10
                    ),
                ], width=15, lg=7),  # Map takes up 6 columns on large screens, full width on smaller ones
  # Make the column a flex container
                ], style={'backgroundColor': '#545646'})
    ),
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("Action Required")),
        dbc.ModalBody("Please select a trail before uploading."),
        dbc.ModalFooter(dbc.Button("Close", id="close-modal", className="ms-auto", n_clicks=0))
    ], id="modal", is_open=False),
    dbc.Modal([
        dbc.ModalHeader("Location Sharing Required"),
        dbc.ModalBody("You need to share your location before getting real-time updates."),
        dbc.ModalFooter(dbc.Button("OK", id="close-location-modal", className="ms-auto", n_clicks=0))
    ], id="location-error-modal", is_open=False),
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("Too Far From Trail")),
        dbc.ModalBody("You are too far from the selected trail to upload images."),
        dbc.ModalFooter(
            dbc.Button("Close", id="close-too-far-modal", className="ms-auto", n_clicks=0)
        )
    ], id="too-far-modal", is_open=False),
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("Congratulations on your find!")),
        dbc.ModalBody([
            html.Img(id="uploaded-image", style={'width': '100%', 'height': 'auto'}),
            html.H4(id="uploaded-species-name", className='mt-2'),
            html.H5(id='uploaded-species-identity'),
            html.P(id="uploaded-species-description")
        ]),
        dbc.ModalFooter(
            dbc.Button("Close", id="close-img-modal", className="ms-auto", n_clicks=0, style={'text-decoration': 'none', 'padding': '5px 15px', 'background': '#545646', 'color': '#F9F1E8', 'border-radius': '20px'})
        )
    ], id="uploaded-img-modal", is_open=False),
    dcc.Interval(
        id='interval-component',
        interval=2*1000,  # in milliseconds, e.g., 5*1000 for 5 seconds
        n_intervals=0
    )
])


@callback(
    [Output('upload-image', 'style'),
     Output('tooltip-upload', 'is_open'),
     Output('tooltip-upload', 'style')],
    [Input('geo', 'position'),
     Input('mytrail-search-dropdown', 'value'),
     Input('section-search-dropdown', 'value')],
    [State('upload-image', 'style')]
)
def update_upload_style_and_tooltip(position, trail_value, section_value, style):
    # Check if both the location is shared (position is not None) and a trail is selected (trail_value is not None)
    if position and trail_value:
        gpx_path = os.path.join('data/trails', f'{trail_value}.gpx')
        trail_points = gpx_to_points(gpx_path).coords
        user_position = (position['lat'], position['lon'])
        if is_within_distance(user_position, trail_points) or section_value:
            return {'display': 'block', 'width': '100%', 'height': '50px',
                    'color': '#545646', 'backgroundColor': '#e8dfd4', 'lineHeight': '50px',
                    'border': 'none', 'borderRadius': '20px', 'textAlign': 'center', 'pointerEvents': 'auto',
                    'cursor': 'pointer', 'transition': 'all 0.2s ease-in-out', 'opacity': '1'}, False, {'display': 'none'}
        elif not section_value:
            return {'display': 'block', 'width': '100%', 'height': '50px',
                'color': '#545646', 'backgroundColor': '#e8dfd4', 'lineHeight': '50px',
                'border': 'none', 'borderRadius': '20px', 'textAlign': 'center', 'pointerEvents': 'none',
                'cursor': 'not-allowed', 'transition': 'all 0.2s ease-in-out', 'opacity': '0.6'}, False, {'display': 'block'}
    elif position and not trail_value:
        return {'display': 'block', 'width': '100%', 'height': '50px',
                'color': '#545646', 'backgroundColor': '#e8dfd4', 'lineHeight': '50px',
                'border': 'none', 'borderRadius': '20px', 'textAlign': 'center', 'pointerEvents': 'none',
                'cursor': 'not-allowed', 'transition': 'all 0.2s ease-in-out', 'opacity': '0.6'}, False, {'display': 'block'}
    elif trail_value and not position:
        return {'display': 'block', 'width': '100%', 'height': '50px',
                'color': '#545646', 'backgroundColor': '#e8dfd4', 'lineHeight': '50px',
                'border': 'none', 'borderRadius': '20px', 'textAlign': 'center', 'pointerEvents': 'none',
                'cursor': 'not-allowed', 'transition': 'all 0.2s ease-in-out', 'opacity': '0.6'}, False, {'display': 'block'}
    else:
        return {'display': 'block', 'width': '100%', 'height': '50px',
                'color': '#545646', 'backgroundColor': '#e8dfd4', 'lineHeight': '50px',
                'border': 'none', 'borderRadius': '20px', 'textAlign': 'center', 'pointerEvents': 'none',
                'cursor': 'not-allowed', 'transition': 'all 0.2s ease-in-out', 'opacity': '0.6'}, False, {'display': 'block'}




@callback(
    Output('location-error-modal', 'is_open'),
    [Input('close-location-modal', 'n_clicks'), Input('geo', 'position_error')],
    [State('location-error-modal', 'is_open')],
    prevent_initial_call=True
)
def toggle_location_error_modal(close_clicks, position_error, is_open):
    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggered_id == 'close-location-modal':
        return False
    elif triggered_id == 'geo' and position_error:
        return True
    return is_open


# @callback(
#     Output('too-far-modal', 'is_open'),
#     [Input('close-too-far-modal', 'n_clicks'),
#      Input('geo', 'position'),
#      Input('mytrail-search-dropdown', 'value')],
#     [State('too-far-modal', 'is_open')],
#     prevent_initial_call=True
# )
# def handle_too_far_modal(close_clicks, position, selected_trail, is_open):
#     ctx = dash.callback_context
#     if not ctx.triggered:
#         raise PreventUpdate
#     triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
#     if triggered_id == 'close-too-far-modal':
#         return False
#     elif triggered_id == 'geo':
#         if not position or not selected_trail:
#             return False
#         gpx_path = os.path.join('data/trails', f'{selected_trail}.gpx')
#         trail_points = gpx_to_points(gpx_path).coords
#         user_position = (position['lat'], position['lon'])
#         if is_within_distance(user_position, trail_points):
#             return False
#         else:
#             return True
#     return is_open

@callback(
    Output('too-far-section', 'style'),
    [Input('geo', 'position'),
     Input('mytrail-search-dropdown', 'value')],
    # [State('too-far-modal', 'is_open')],
    prevent_initial_call=True
)
def show_upload_options(position, trail_name):
    if not trail_name:
        return dash.no_update
    gpx_path = os.path.join('data/trails', f'{trail_name}.gpx')
    trail_points = gpx_to_points(gpx_path).coords
    user_position = (position['lat'], position['lon'])
    if not is_within_distance(user_position, trail_points):
        return {'display':'block', 'margin':'10%'}
    else:
        return {'display': 'none'}

# @callback(
#     Output('uploaded-img-modal', 'is_open'),
#     [Input('close-img-modal', 'n_clicks')],
#     [State('uploaded-img-modal', 'is_open')]
# )
# def close_uploaded_img_modal(n_clicks, is_open):
#     if n_clicks:
#         return False
#     return is_open
  
@callback(
    [Output('upload-status', 'children'),
     Output('uploaded-img-modal', 'is_open'),
     Output('uploaded-image', 'src'),
     Output('uploaded-species-name', 'children'),
     Output('uploaded-species-identity', 'children'),
     Output('uploaded-species-description', 'children')],
    [Input('upload-image', 'contents'),
     Input('geo', 'local_date'),
     Input('section-search-dropdown', 'value'),
     Input('close-img-modal', 'n_clicks')],
    [State('geo', 'position'),
     State('geo', 'position_error'),
     State('mytrail-search-dropdown', 'value'),
     State('uploaded-img-modal', 'is_open')],
    prevent_initial_call=True
)
def handle_image_and_modal(contents, local_date, section_value, close_n_clicks, position, position_error, selected_trail, modal_is_open):
    triggered_id = callback_context.triggered[0]['prop_id'].split('.')[0]

    if triggered_id == 'close-img-modal':
        return dash.no_update, False, dash.no_update, dash.no_update, dash.no_update, dash.no_update
    if contents is None:
        return "", False, None, None, None, None
    if position_error:
        return "Failed to get geolocation data.", False, None, None, None, None
    content_type, content_string = contents[0].split(',')
    decoded = base64.b64decode(content_string)

    if not selected_trail:
        return "Please select a trail.", False, None, None, None, None

    gpx_path = os.path.join('data/trails', f'{selected_trail}.gpx')
    trail_points = gpx_to_points(gpx_path).coords

    # Check if user is within a reasonable distance of the trail
    if position and is_within_distance((position['lat'], position['lon']), trail_points):
        latitude = position['lat']
        longitude = position['lon']
        is_far = False
    else:
        # If no section is selected, prompt the user to select a section
        if not section_value:
            return "You're too far from the trail. Please select a section.", False, None, None, None, None

        # Determine approximate location based on section selected
        if section_value == 'Towards the beginning':
            approximate_point = int(len(trail_points) * 1/3)
        elif section_value == 'Somewhere in the middle of the trail':
            approximate_point = int(len(trail_points) * 1/2)
        elif section_value == 'Only at the end':
            approximate_point = int(len(trail_points) * 2/3)
        else:
            return "Please select the approximate section of the trail.", False, None, None, None, None

        latitude, longitude = trail_points[approximate_point]
        is_far = False

    try:
        output_text = detect_labels(decoded)
        if output_text == 'None':
            return "There was a problem with your image, try again.", True, None, 'There was a problem with the image, please try again!', None, None
        else:
            species_name = output_text.split('|')[0].strip()
            species_identity = output_text.split('|')[1].strip()
            species_desc = output_text.split('|')[-1].strip()
    except:
        return "There was a problem with your image, try again.", True, None, 'There was a problem with the image, please try again!', None, None

    try:
        session = Session()
        last_row = session.query(Uploads).order_by(Uploads.upload_id.desc()).first()
        last_row_id = last_row.upload_id if last_row else 0
        new_upload = Uploads(
            upload_id=last_row_id + 1,
            upload_lat=latitude,
            upload_long=longitude,
            upload_time=datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            upload_img=decoded,
            upload_species=species_name,
            upload_identity=species_identity,
            upload_desc=species_desc
        )
        session.add(new_upload)
        session.commit()
        session.close()
    except SQLAlchemyError as e:
        session.rollback()
        session.close()
        return "There was a problem with your image, try again.", True, None, 'There was a problem with the image, please try again!', None, None

    return "Image uploaded successfully!", True, contents[0], species_name, species_identity, species_desc

# Add a callback to close the modal
# @callback(
#     Output('too-far-modal', 'is_open'),
#     [Input('close-select-section-modal', 'n_clicks')],
#     [State('too-far-modal', 'is_open')]
# )
# def close_select_section_modal(n_clicks, is_open):
#     if n_clicks:
#         return not is_open
#     return is_open

# @callback(
#     # Output('upload-status', 'children'),  # An Output to indicate the upload status
#     # [Input('upload-image', 'contents'),  # Contents from the upload component
#     #  Input('geo', 'local_date')],  # Date from the geolocation component
#     # [State('geo', 'position'),  # Position state from geolocation
#     #  State('geo', 'position_error')],  # Position error state from geolocation
#     # prevent_initial_call=True
#     Output('upload-status', 'children'),
#     [Input('upload-image', 'contents'),
#      Input('geo', 'local_date'),
#      Input('section-search-dropdown', 'value')],
#     [State('geo', 'position'),
#      State('geo', 'position_error'),
#      State('mytrail-search-dropdown', 'value')],
#     prevent_initial_call=True
# )
# def handle_upload(contents, local_date, section_value, position, position_error, selected_trail):
#     if contents is None:
#         # If no image is uploaded, do nothing
#         return ""
#     if position_error:
#         # Handle case where geolocation failed
#         return "Failed to get geolocation data."
#     content_type, content_string = contents[0].split(',')  # Taking the first uploaded file
#     image_bytes = content_string  # base64 encoded string of the first image
#     # latitude = position['lat']
#     # longitude = position['lon']
#         # Check if user is within a reasonable distance of the trail
    
#     gpx_path = os.path.join('data/trails', f'{selected_trail}.gpx')
#     trail_points = gpx_to_points(gpx_path).coords
    
#     if position and is_within_distance((position['lat'], position['lon']), trail_points):
#         latitude = position['lat']
#         longitude = position['lon']
#     else:
#         # Determine approximate location based on section selected
#         if section_value == 'Towards the beginning':
#             approximate_point = int(len(trail_points) * 1/3)
#         elif section_value == 'Somewhere in the middle of the trail':
#             approximate_point = int(len(trail_points) * 1/2)
#         elif section_value == 'Only at the end':
#             approximate_point = int(len(trail_points) * 2/3)
#         else:
#             return "Please select the approximate section of the trail."
#         latitude, longitude = trail_points[approximate_point]
        
#     decoded = base64.b64decode(content_string)
#     try:
#         detected_labels = detect_labels(decoded)
#         labels = [l.description.lower() for l in detected_labels]
#         if len(set(labels).intersection(set(get_unique_species(df_trails)))):
#             species = list(set(labels).intersection(set(get_unique_species(df_trails))))[0].capitalize()
#         else:
#             species = detected_labels[0].description
#     except:
#         return "There was a problem in your image, try again"
#     try:
#         session = Session()
#         # Attempt to fetch data within a transaction
#         # session.begin()  # Start a new transaction
#         last_row = session.query(Uploads).order_by(Uploads.upload_id.desc()).first()
#         last_row_id = last_row.upload_id
#         new_upload = Uploads(
#             upload_id=last_row_id+1,
#             upload_lat=latitude,
#             upload_long=longitude,
#             upload_time=datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
#             upload_img=decoded,
#             upload_species=species
#         )
#         session.add(new_upload)
#         session.commit()
#         session.close()
#     except SQLAlchemyError as e:
#         session = Session()
#         session.rollback()  # Roll back the transaction if an error occurs
#         session.close()
#         # print("Error fetching data from the database: ", e)
#         return "There was a problem in your image, try again"

#     return "Image uploaded successfully!"


@callback(
    Output('myimage-layer', 'children'),
    [Input('upload-image', 'contents'),
     Input('mytrail-search-dropdown', 'value'),
     Input('geo', 'position'),
     Input('interval-component', 'n_intervals')],
    [State('mytrail-map', 'zoom')]
)
def display_image_marker(contents, trail, user_position, n, zoom):
    # print(user_position)
    if not trail:
        return []

    markers = []
    if user_position:
        # print('entered here in user')
        user_marker = dl.Marker(
            position=(user_position['lat'], user_position['lon']),
            icon={"iconUrl": 'assets/hiker.png', "iconSize": [zoom * 4, zoom * 4]},
            # icon={"iconUrl": html.I(className="fas fa-clock"), "iconSize": [zoom * 4, zoom * 4]},
            children=[
                dl.Tooltip("You are here"),
                dl.Popup(f"Your location: Latitude {user_position['lat']}, Longitude {user_position['lon']}")
            ])
        markers.append(user_marker)

    # Load trail GPX data
    gpx_path = os.path.join('data/trails', f'{trail}.gpx')
    trail_points = gpx_to_points(gpx_path).coords
    start_marker = dl.Marker(position=trail_points[0], children=[dl.Tooltip("Start")], icon={"iconUrl": 'assets/start.png', "iconSize": [zoom * 10, zoom * 10]})
    end_marker = dl.Marker(position=trail_points[-1], children=[dl.Tooltip("Finish")], icon={"iconUrl": 'assets/finish.png', "iconSize": [zoom * 10, zoom * 10]})
    markers.extend([start_marker, end_marker])

    # Fetch upload data with retry logic
    uploads = fetch_data(Uploads)
    if uploads:
        for upload in uploads:
            if is_within_distance((upload.upload_lat, upload.upload_long), trail_points):
                image_url = db_img(upload.upload_img)
                if upload.upload_identity == 'Dangerous':
                    species_marker = dl.Marker(
                        position=(upload.upload_lat, upload.upload_long),
                        children=[dl.Tooltip(children=
                                             [html.Img(src=image_url, style={'width': '100px', 'height': 'auto'}), html.P(""), 
                                              upload.upload_species, html.P(""),
                                              upload.upload_identity])],
                        icon={"iconUrl": 'assets/dangerous_species.png', "iconSize": [zoom * 7, zoom * 5]})
                    markers.append(species_marker)
                elif upload.upload_identity == 'Endangered':
                    species_marker = dl.Marker(
                        position=(upload.upload_lat, upload.upload_long),
                        children=[dl.Tooltip(children=
                                             [html.Img(src=image_url, style={'width': '100px', 'height': 'auto'}), html.P(""), 
                                              upload.upload_species, html.P(""),
                                              upload.upload_identity])],
                        icon={"iconUrl": 'assets/endangered_species.png', "iconSize": [zoom * 7, zoom * 5]})
                    markers.append(species_marker)
                elif upload.upload_identity == 'Safe':
                    species_marker = dl.Marker(
                        position=(upload.upload_lat, upload.upload_long),
                        children=[dl.Tooltip(children=
                                             [html.Img(src=image_url, style={'width': '100px', 'height': 'auto'}), html.P(""), 
                                              upload.upload_species, html.P(""),
                                              upload.upload_identity])],
                        icon={"iconUrl": 'assets/safe_species.png', "iconSize": [zoom * 7, zoom * 5]})
                    markers.append(species_marker)

    print(f"Total markers for trail '{trail}': {len(markers)}")
    return markers

@callback(
    [Output('mytrail-layer', 'children'), Output("mytrail-map", "viewport")],
    [Input('mytrail-search-dropdown', 'value')]
)
def update_map(trail_name):
    if not trail_name:
        return [], dash.no_update

    # Load the GPX data
    gpx_path = os.path.join('data/trails', f'{trail_name}.gpx')
    line_string = gpx_to_points(gpx_path)
    centroid = line_string.centroid.coords[0]
    positions = list(line_string.coords)
    features = [dl.Polyline(positions=positions, color='blue')]

    # Calculate the bounds for zoom estimation
    min_lat = min(point[1] for point in positions)
    max_lat = max(point[1] for point in positions)
    min_lon = min(point[0] for point in positions)
    max_lon = max(point[0] for point in positions)
    bounds = [[min_lat, min_lon], [max_lat, max_lon]]

    # Estimate zoom level based on bounds
    estimated_zoom = estimate_zoom(min_lat, max_lat, min_lon, max_lon)
    # print(f"Center: {centroid}, Estimated Zoom: {estimated_zoom}")

    return features, dict(center=centroid, zoom=estimated_zoom, transition="flyTo")
