from dash_extensions.enrich import DashProxy
from dash_extensions import Purify, DeferScript
from dash import html
import pandas as pd
import dash
import base64
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, ALL
from dash.exceptions import PreventUpdate
from datetime import datetime

df_events = pd.read_csv('data/event_data.csv')
# Group the cards into chunks of 4
chunks = [df_events.iloc[i:i+4] for i in range(0, df_events.shape[0], 4)]

dash.register_page(__name__, title='WildStep Events')

# Create a list of dbc.Rows, each containing 4 cards
tabs = dbc.Tabs(
    [
        dbc.Tab(
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardImg(src=row["Image"], top=True, alt="Event image", style={'height': '200px', 'object-fit': 'cover'}),
                                dbc.CardBody([
                                    html.H4(row["Title"], className="card-title"),
                                    html.P(f"Date: {row['Date']}", className="card-text"),
                                    html.P(f"Location: {row['Location']}", className="card-text"),
                                    dbc.Button("More Info", color="primary", href=row["URL"], target="_blank")
                                ])
                            ],
                            style={"width": "18rem"},  # Fixed width for consistency
                            className="m-3 mb-4 d-flex flex-column"  # Margin for spacing
                        )
                    ) for _, row in chunk.iterrows() if pd.notna(row["Image"])  # Check if image URL is not NaN
                ],
                className="justify-content-center"
            ), 
            label=f"The upcoming event", tab_class_name="tab-label"
        ) for i, chunk in enumerate(chunks[:1])
    ]  
)

today = datetime.now().strftime('%Y-%m-%d')
# filtered_events = df_events[df_events['Date'] == today]

carousel_items = [
    {
        'key': str(index),
        'src': row["Image"],
        'header': row["Title"],
        'caption': f"Date: {row['Date']} | Location: {row['Location']}",
        'img_style': {'opacity':'0.3'},
        'href': row['URL'],
        'external_link': True,
    }
    for index, row in df_events.iterrows() if pd.notna(row["Image"])
]
 
# Create the carousel using the new items list.
carousel = dbc.Carousel(
    items=carousel_items,
    controls=True,  # Enable navigation controls.
    indicators=True,  # Show indicators.
    interval=4000,  # Time in milliseconds between item cycles.
    ride='carousel',
    className="carousel-fade"
)

def b64_image(img):
    with open(img, 'rb') as f:
        image = f.read()
    return 'data:image/png;base64,' + base64.b64encode(image).decode('utf-8')

app = DashProxy(assets_folder='assets')
layout = html.Div([
            dbc.Row([
                dbc.Col([
                    html.Div(style={'position': 'relative', 'width': '90%', 'margin-top': '10%', 'margin-left': '5%'}, children=[
                    html.Img(src=b64_image('assets/events_species.png'), style={'width':'100%', 'height':'auto', 'opacity':'0.3', 'borderRadius':'50px'}),
                    html.Div("SAVE", style={
                        'position': 'absolute',
                        'top': '10%',
                        'left':'5%',
                        'color': '#545646',
                        'font-size': '4vw',
                        'text-align': 'left',
                        'font-weight':'bold',
                        'text-shadow': '-1px -1px 0 #000, 1px -1px 0 #000, -1px 1px 0 #000, 1px 1px 0 #000'
                    }),
                    html.Div("VICTORIAN", style={
                        'position': 'absolute',
                        'top': '37%',
                        'left':'5%',
                        'color': '#545646',
                        'font-size': '4vw',
                        'text-align': 'left',
                        'font-weight':'bold',
                        'text-shadow': '-1px -1px 0 #000, 1px -1px 0 #000, -1px 1px 0 #000, 1px 1px 0 #000'
                    }),
                    html.Div("BIODIVERSITY", style={
                        'position': 'absolute',
                        'top': '65%',
                        'left':'5%',
                        'color': '#545646',
                        'font-size': '4vw',
                        'text-align': 'left',
                        'font-weight':'bold',
                        'text-shadow': '-1px -1px 0 #000, 1px -1px 0 #000, -1px 1px 0 #000, 1px 1px 0 #000'
                    })
                ])
                    ], width=7),
                dbc.Col([
                    html.P("Include Victoria's diverse biodiversity in your weekend plans", style={'margin-top':'12%', 'font-size':'2vw', 'color': '#545646', 'padding':'5%', 'text-align':'center', 'font-weight':'bold',}),
                    html.P("Participate in conservation events or view seasonal wildlife activities around you. Scroll to browse through upcoming events or view the calendar for all events", style={'font-size':'1.3vw', 'color': '#545646', 'text-align':'center', 'padding':'5%'}),
                #     html.Div(children=[
                #         html.Img(src=b64_image('assets/element3.png'), style={'width': '50%', 'height': 'auto', 'margin-left':'20%', 'margin-top':'5%'}),
                #         html.P("Did you know the number of endangered species", style={'margin-top': '5%', 'left': '55%', 'font-size':'20px', 'text-color':'#F9F1E8'}),
                #         # html.P("Discover conservation events around you", className="hover-text", style={'top': '55%', 'left': '55%'})
                # ], id='left1')
            ], width=5),
        ]),
        dbc.Row([
                dbc.Col([
                    html.Div([
                        html.P("Browse through all upcoming conservation and seasonal events in Victoria", style={'margin-top':'40%', 'margin-left':"27%", 'font-size':'2vw', 'color': '#545646','text-align':'center', 'font-weight':'bold',}),
                    ]) 
                ], width=4),
                dbc.Col([
                    dbc.Container([carousel], fluid=True, style={'padding':'10%'}),
            ], width=8),
                
        ]),
        
    
    
    
    # dbc.Container([tabs 
    #     ],
    #     fluid=True,
    #     style={'marginTop': '50px', 'marginBottom': '50px'}  
    # ),
    html.Div(className="card card-calendar", style={"height": "10%", 'margin':'5%'}, children=[
        html.Div(className="card-body p-3", children=[
            html.Div(id="calendar", **{"data-bs-toggle": "calendar"})
        ])
    ]),
    DeferScript(src='assets/full_calendar_deferscript.js')              
])



# if __name__ == "__main__":
#     app.run_server()
