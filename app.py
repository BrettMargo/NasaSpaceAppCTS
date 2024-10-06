import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Load the dataset with all Canadian places (cities, towns, villages, etc.)
canadian_places = pd.read_csv('canadacities.csv')

# Load and filter soil moisture data from the initial file
canada_soil_moisture = pd.read_csv('./can_smap_today.csv')
import plotly.express as px

def create_map(data):
    # Define a custom color scale: brown to blue
    custom_color_scale = [
        [0, 'brown'],    # Value 0 corresponds to brown
        [0.5, 'beige'],  # Value 0.5 corresponds to beige
        [1, 'blue']      # Value 1 corresponds to blue
    ]

    fig = px.scatter_mapbox(
        data,
        lon='Longitude',
        lat='Latitude',
        color='Soil_Moisture',
        color_continuous_scale=custom_color_scale,  # Use the custom color scale
        size_max=15,
        title="Soil Moisture Data in Canada",
        labels={'Soil_Moisture': 'Soil Moisture'},
    )


    fig.update_layout(
        mapbox_style="open-street-map",
        mapbox_zoom=3,
        mapbox_center={"lat": 56.1304, "lon": -106.3468},  # Center on Canada
    )
    # Add color bar
    fig.update_layout(coloraxis_colorbar=dict(title='Soil Moisture'))
    return fig


# Initial map
fig = create_map(canada_soil_moisture)

# Define crop names for the dropdown
crop_names = ['Wheat', 'Corn', 'Barley', 'Soybean', 'Oats', 'Canola']

# Dash app setup
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Interactive Soil Moisture Map"),
    # Wrapper for the dropdowns arranged horizontally
    html.Div([
        dcc.Dropdown(
            id='place-dropdown',
            options=[{'label': place, 'value': place} for place in canadian_places['city']],
            placeholder='Search for a place in Canada',
            multi=False,
            clearable=True,
            style={'width': '300px'}  # Optional: set width for better alignment
        ),
        dcc.Dropdown(
            id='crop-dropdown',
            options=[{'label': crop, 'value': crop} for crop in crop_names],
            placeholder='Select a crop',
            multi=False,
            clearable=True,
            style={'width': '300px'}  # Optional: set width for better alignment
        ),
        dcc.Dropdown(
            id='data-dropdown',
            options=[
                {'label': 'Today\'s Data', 'value': 'can_smap_today.csv'},
                {'label': 'Week Ahead Data', 'value': 'can_smap_week.csv'}
            ],
            placeholder='Select data source',
            multi=False,
            clearable=True,
            style={'width': '300px'}  # Optional: set width for better alignment
        ),
    ], style={'display': 'flex', 'flex-direction': 'row', 'gap': '10px', 'margin-bottom': '20px'}),  # Stack horizontally
    dcc.Graph(
        id='map',
        figure=fig,
        style={'height': '80vh', 'width': '100%'}  # Set the height to 80% of the viewport height
    ),
])

# Callback to update the map when a place is selected or data source is changed
@app.callback(
    Output('map', 'figure'),
    [Input('place-dropdown', 'value'),
     Input('data-dropdown', 'value')]
)
def update_map(selected_place, selected_data):
    # Load the selected data
    global canada_soil_moisture
    if selected_data:
        canada_soil_moisture = pd.read_csv(selected_data)
    
    # Create a new figure for the map
    fig = create_map(canada_soil_moisture)

    if selected_place:
        print(selected_place)
        place_info = canadian_places[canadian_places['city'] == selected_place].iloc[0]

        # Zoom level - increase dot size as you zoom in
        zoom_level = 8
        
        # Adjust the size of the markers based on the zoom level
        fig.update_traces(marker=dict(size=[zoom_level * 1.5 for _ in range(len(canada_soil_moisture))]))

        # Update the map to zoom into the place's location
        fig.update_layout(
            mapbox_center={"lat": place_info['lat'], "lon": place_info['lng']},
            mapbox_zoom=zoom_level,
        )

    return fig

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
