import folium
import requests

# Coordenadas geográficas de la planta Clarkson Grain Mattoon.
# Se usarán como punto central del mapa y para colocar un marcador.
lat, lon = 39.481427, -88.303999

# Crear un mapa centrado en las coordenadas dadas.
# zoom_start define el nivel inicial de acercamiento.
m = folium.Map(location=[lat, lon], zoom_start=7)

# Texto HTML que se mostrará al hacer clic en el marcador.
# Incluye información descriptiva del punto.
popup_text = (
    "<b>Clarkson Grain Mattoon Plant</b><br>"
    "Ubicación: Mattoon, Illinois<br>"
    "Latitud: 39.481427<br>"
    "Longitud: -88.303999<br>"
    "Tipo: Centro de acopio de granos."
)

# Añadir un marcador al mapa en la ubicación especificada.
# popup: ventana emergente con detalles.
# tooltip: texto que aparece al pasar el cursor.
# icon: personaliza el ícono del marcador (color y símbolo de FontAwesome).
folium.Marker(
    [lat, lon],
    popup=popup_text,
    tooltip="Clarkson Grain Mattoon Plant",
    icon=folium.Icon(color="green", icon="leaf", prefix="fa")
).add_to(m)

# Descargar un archivo GeoJSON que contiene los límites de los estados de EE. UU.
# Folium puede usar estos datos para dibujar polígonos en el mapa.
url = "https://raw.githubusercontent.com/python-visualization/folium/main/examples/data/us-states.json"
geojson_data = requests.get(url).json()

# Añadir capas GeoJSON al mapa y resaltar el estado de Illinois.
# style_function: define el estilo visual por defecto (color, opacidad, etc.)
# highlight_function: estilo cuando el usuario pasa el mouse por encima.
# tooltip: muestra el nombre del estado cuando el cursor lo toca.
folium.GeoJson(
    geojson_data,
    name="Illinois",
    style_function=lambda feature: {
        # Pintar Illinois de verde y los demás estados en gris.
        "fillColor": "green" if feature["id"] == "IL" else "gray",
        "color": "black",        # Contorno del estado
        "weight": 1,             # Grosor del contorno
        # Opacidad más alta para Illinois para destacarlo.
        "fillOpacity": 0.3 if feature["id"] == "IL" else 0.05,
    },
    highlight_function=lambda feature: {
        # Cambiar estilo al pasar el cursor sobre cualquier estado.
        "weight": 2,
        "color": "black",
        "fillOpacity": 0.6 if feature["id"] == "IL" else 0.1,
    },
    tooltip=folium.GeoJsonTooltip(fields=["name"]),
).add_to(m)

# Añadir un control de capas para alternar la visualización del GeoJSON
# u otros elementos si se agregaran más capas.
folium.LayerControl().add_to(m)

# Guardar el mapa generado como un archivo HTML.
m.save("centro_de_acopio.html")
