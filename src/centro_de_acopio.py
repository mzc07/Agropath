import folium
import requests

# Coordenadas del Clarkson Grain Mattoon Plant
lat, lon = 39.481427, -88.303999

# Crear mapa centrado en la planta
m = folium.Map(location=[lat, lon], zoom_start=7)

# Añadir marcador con información
popup_text = (
    "<b>Clarkson Grain Mattoon Plant</b><br>"
    "Ubicación: Mattoon, Illinois<br>"
    "Latitud: 39.481427<br>"
    "Longitud: -88.303999<br>"
    "Tipo: Centro de acopio de granos."
)

folium.Marker(
    [lat, lon],
    popup=popup_text,
    tooltip="Clarkson Grain Mattoon Plant",
    icon=folium.Icon(color="green", icon="leaf", prefix="fa")
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
m.save("centro_de_acopio.html")
