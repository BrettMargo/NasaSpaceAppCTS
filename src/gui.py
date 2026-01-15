import csv
import pandas as pd
from nicegui import ui

# Load and filter soil moisture data
canada_soil_moisture = pd.read_csv('./can_smap_today.csv')

# Convert soil moisture data to the required format
moisture_data = canada_soil_moisture[['Latitude', 'Longitude', 'Soil_Moisture']].values.tolist()

# Function to update the map with the heatmap layer
async def update_map_with_heatmap(data):
    # Prepare the heatmap JavaScript to overlay on the map
    heatmap_js = f"""
    var heat = L.heatLayer({data}, {{
        radius: 25,
        blur: 15,
        maxZoom: 20
    }}).addTo(map);
    """
    await ui.run_javascript(heatmap_js)

m = ui.leaflet(center=(50.095, -112.183)).style('height: 450px; width: 100%; background-color: lightblue;')
m.clear_layers()
m.tile_layer(
    url_template=r'https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png',
    options={
        'maxZoom': 20,
        'attribution':
            'Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, <a href="https://viewfinderpanoramas.org/">SRTM</a> | '
            'Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)'
    },
)
m.generic_layer(name='circle', args=[m.center, {'color': 'red', 'radius': 400}])

m.tile_layer(heatmap_data, {'radius': 25, 'blur': 15, 'maxZoom': 20})

ui.label().bind_text_from(m, 'center', lambda center: f'Center: {center[0]:.3f}, {center[1]:.3f}')
ui.label().bind_text_from(m, 'zoom', lambda zoom: f'Zoom: {zoom}')

dark=ui.dark_mode()
dark.enable()

with ui.grid(columns=4):
    ui.button(icon='zoom_in', on_click=lambda: m.set_zoom(m.zoom + 1))
    ui.button(icon='zoom_out', on_click=lambda: m.set_zoom(m.zoom - 1))
    ui.button('Dark', on_click=dark.enable)
    ui.button('Light', on_click=dark.disable)

ui.run()