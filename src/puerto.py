import folium
import requests

# Coordenadas del Puerto de Metropolitan St. Louis
lat, lon = 38.61, -90.20

# Crear mapa centrado en el puerto
m = folium.Map(location=[lat, lon], zoom_start=6)

# Añadir marcador con información
popup_text = (
    "<b>Port of Metropolitan St. Louis</b><br>"
    "Ubicación: Port of Metropolitan St. Louis<br>"
    "Latitud: 38.61° N<br>"
    "Longitud: 90.20° W<br>"
    "Tipo: Puerto fluvial en el río Misisipi."
)
folium.Marker(
    [lat, lon],
    popup=popup_text,
    tooltip="Port of Metropolitan St. Louis",
    icon=folium.Icon(color="green", icon="anchor", prefix="fa")
).add_to(m)

# Descargar shapefile GeoJSON de los estados de EE. UU.
url = "https://raw.githubusercontent.com/python-visualization/folium/main/examples/data/us-states.json"
geojson_data = requests.get(url).json()

# Resaltar Illinois en verde
folium.GeoJson(
    geojson_data,
    name="Illinois",
    style_function=lambda feature: {
        "fillColor": "green" if feature["id"] == "IL" else "gray",
        "color": "black",
        "weight": 1,
        "fillOpacity": 0.3 if feature["id"] == "IL" else 0.05,
    },
    highlight_function=lambda feature: {
        "weight": 2,
        "color": "black",
        "fillOpacity": 0.6 if feature["id"] == "IL" else 0.1,
    },
    tooltip=folium.GeoJsonTooltip(fields=["name"]),
).add_to(m)

# Mostrar capa de control
folium.LayerControl().add_to(m)

# Guardar mapa en HTML
m.save("puerto_st_louis.html")

