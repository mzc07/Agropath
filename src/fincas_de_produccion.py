import folium
import requests

# Datos de las fincas
fincas = [
    {"nombre": "Finca 1", "lat": 40.92, "lon": -89.53, "info": "Parcela de producción"},
    {"nombre": "Finca 2", "lat": 40.92, "lon": -89.54, "info": "Parcela de producción"},
    {"nombre": "Finca 3", "lat": 40.91, "lon": -89.53, "info": "Parcela de producción"},
    {"nombre": "Finca 4", "lat": 40.91, "lon": -89.52, "info": "Parcela de producción"},
    {"nombre": "Finca 5", "lat": 40.91, "lon": -89.54, "info": "Parcela de producción"},
    {"nombre": "Finca 6", "lat": 40.91, "lon": -89.55, "info": "Parcela de producción"},
    {"nombre": "Finca 7", "lat": 40.91, "lon": -89.51, "info": "Parcela de producción"},
]

# Crear mapa centrado en Illinois
m = folium.Map(location=[40.0, -89.0], zoom_start=7)

# Descargar GeoJSON con los límites reales de los estados de EE.UU.
url = "https://raw.githubusercontent.com/python-visualization/folium/main/examples/data/us-states.json"
geojson_data = requests.get(url).json()

# Resaltar Illinois con su forma real y permitir selección al hacer clic
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

# Agregar los puntos de las fincas
for finca in fincas:
    folium.Marker(
        location=[finca["lat"], finca["lon"]],
        popup=f"<b>{finca['nombre']}</b><br>{finca['info']}",
        tooltip=finca["nombre"],
        icon=folium.Icon(color="red", icon="info-sign")
    ).add_to(m)

# Capa de control
folium.LayerControl().add_to(m)

# Guardar mapa
m.save("mapa_fincas_illinois.html")

