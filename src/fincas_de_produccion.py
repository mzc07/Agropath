import folium
import requests

# Lista de fincas con su información básica.
# Cada finca contiene: nombre, latitud, longitud y una breve descripción.
# Esta estructura permite iterar fácilmente y agregar marcadores al mapa.
fincas = [
    {"nombre": "Finca 1", "lat": 40.92, "lon": -89.53, "info": "Parcela de producción"},
    {"nombre": "Finca 2", "lat": 40.92, "lon": -89.54, "info": "Parcela de producción"},
    {"nombre": "Finca 3", "lat": 40.91, "lon": -89.53", "info": "Parcela de producción"},
    {"nombre": "Finca 4", "lat": 40.91, "lon": -89.52", "info": "Parcela de producción"},
    {"nombre": "Finca 5", "lat": 40.91, "lon": -89.54", "info": "Parcela de producción"},
    {"nombre": "Finca 6", "lat": 40.91, "lon": -89.55", "info": "Parcela de producción"},
    {"nombre": "Finca 7", "lat": 40.91, "lon": -89.51", "info": "Parcela de producción"},
]

# Crear un mapa base usando Folium.
# 'location' define el punto central del mapa y 'zoom_start' el nivel de zoom inicial.
# En este caso, se ubica el centro sobre Illinois.
m = folium.Map(location=[40.0, -89.0], zoom_start=7)

# URL donde se encuentra alojado un archivo GeoJSON que contiene los límites de los estados de EE. UU.
# Se descarga para poder dibujar sobre el mapa la forma real del estado de Illinois.
url = "https://raw.githubusercontent.com/python-visualization/folium/main/examples/data/us-states.json"
geojson_data = requests.get(url).json()  # Se obtiene el contenido como un diccionario Python.

# Crear una capa GeoJson para mostrar los límites estatales.
# style_function define el estilo visual de cada estado.
#   - Si el estado es Illinois (id = "IL"), se pinta en verde con mayor opacidad.
#   - El resto se muestra gris y con menos opacidad.
# highlight_function define cómo se ve un estado al pasar el cursor por encima.
# tooltip muestra el nombre del estado al pasar el mouse.
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

# Agregar un marcador para cada finca en el mapa.
# folium.Marker coloca un punto en el mapa usando latitud y longitud.
# popup permite mostrar información detallada al hacer clic.
# tooltip muestra el nombre de la finca al pasar el mouse.
# icon permite personalizar el marcador; aquí se usa color rojo.
for finca in fincas:
    folium.Marker(
        location=[finca["lat"], finca["lon"]],
        popup=f"<b>{finca['nombre']}</b><br>{finca['info']}",
        tooltip=finca["nombre"],
        icon=folium.Icon(color="red", icon="info-sign")
    ).add_to(m)

# Añadir un control de capas para poder activar o desactivar visualmente capas del mapa.
folium.LayerControl().add_to(m)

# Guardar el mapa final como un archivo HTML interactivo.
m.save("mapa_fincas_illinois.html")
