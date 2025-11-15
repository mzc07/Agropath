import folium
import requests

# Coordenadas del Puerto de Metropolitan St. Louis.
# Se almacenan en variables separadas para facilitar su uso en varias partes del código.
lat, lon = 38.61, -90.20

# Crear el mapa centrado en las coordenadas del puerto.
# folium.Map genera un mapa interactivo basado en Leaflet.js.
# zoom_start define el nivel de zoom inicial.
m = folium.Map(location=[lat, lon], zoom_start=6)

# Crear el texto que aparecerá en el popup del marcador.
# Se usa HTML simple para darle formato.
popup_text = (
    "<b>Port of Metropolitan St. Louis</b><br>"
    "Ubicación: Port of Metropolitan St. Louis<br>"
    "Latitud: 38.61° N<br>"
    "Longitud: 90.20° W<br>"
    "Tipo: Puerto fluvial en el río Misisipi."
)

# Añadir un marcador al mapa.
# folium.Marker coloca un punto interactivo sobre el mapa, con tooltip (al pasar el mouse)
# y popup (al hacer clic).
# Se usa un ícono personalizado de FontAwesome (color verde con símbolo de ancla).
folium.Marker(
    [lat, lon],
    popup=popup_text,
    tooltip="Port of Metropolitan St. Louis",
    icon=folium.Icon(color="green", icon="anchor", prefix="fa")
).add_to(m)

# Descargar un GeoJSON con los límites de los estados de EE. UU.
# Este archivo lo provee el repositorio oficial de ejemplos de Folium.
# Se utiliza requests para obtenerlo mediante HTTP y convertirlo a JSON.
url = "https://raw.githubusercontent.com/python-visualization/folium/main/examples/data/us-states.json"
geojson_data = requests.get(url).json()

# Añadir la capa GeoJSON al mapa.
# style_function define cómo se dibuja cada estado en condiciones normales.
# - Illinois (ID: "IL") se dibuja en verde.
# - El resto de estados se dibujan en gris.
# highlight_function define el estilo al pasar el cursor sobre un estado.
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
    # tooltip muestra el nombre del estado al pasar el mouse.
    tooltip=folium.GeoJsonTooltip(fields=["name"]),
).add_to(m)

# Añadir un control de capas.
# Permite activar o desactivar capas interactuando con un panel en el mapa.
folium.LayerControl().add_to(m)

# Guardar el mapa final como un archivo HTML.
# El archivo puede abrirse en cualquier navegador web.
m.save("puerto_st_louis.html")
