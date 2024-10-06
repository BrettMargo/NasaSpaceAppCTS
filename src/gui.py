from nicegui import ui

m = ui.leaflet(center=(50.095, -112.183))
m.tile_layer(
    url_template=r'https://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
    options={
        "maxZoom": 20,
        "subdomains": ['mt0', 'mt1', 'mt2', 'mt3'],
        "attribution": '© Google'
    },
)
m.generic_layer(name='circle', args=[m.center, {'color': 'red', 'radius': 400}])

ui.label().bind_text_from(m, 'center', lambda center: f'Center: {center[0]:.3f}, {center[1]:.3f}')
ui.label().bind_text_from(m, 'zoom', lambda zoom: f'Zoom: {zoom}')

dark = ui.dark_mode()
ui.label('Switch mode:')
with ui.grid(columns=4):
    ui.button(icon='zoom_in', on_click=lambda: m.set_zoom(m.zoom + 1))
    ui.button(icon='zoom_out', on_click=lambda: m.set_zoom(m.zoom - 1))
    ui.button('Dark', on_click=dark.enable)
    ui.button('Light', on_click=dark.disable)

ui.run()