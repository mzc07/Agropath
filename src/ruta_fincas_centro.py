import requests
import folium
import networkx as nx
from geopy.distance import geodesic
import random

# Lista de fincas con datos básicos.
# Cada finca incluye nombre, coordenadas (lat, lon) e información adicional.
fincas = [
    {"nombre": "Finca 1", "lat": 40.92, "lon": -89.53, "info": "Parcela de producción"},
    {"nombre": "Finca 2", "lat": 40.92, "lon": -89.54, "info": "Parcela de producción"},
    {"nombre": "Finca 3", "lat": 40.91, "lon": -89.53, "info": "Parcela de producción"},
    {"nombre": "Finca 4", "lat": 40.91, "lon": -89.52, "info": "Parcela de producción"},
    {"nombre": "Finca 5", "lat": 40.91, "lon": -89.54, "info": "Parcela de producción"},
    {"nombre": "Finca 6", "lat": 40.91, "lon": -89.55, "info": "Parcela de producción"},
    {"nombre": "Finca 7", "lat": 40.91, "lon": -89.51, "info": "Parcela de producción"},
]

# Coordenadas del centro de acopio (destino final de todas las rutas)
destination = (39.481427, -88.303999)

def get_osrm_route(origin_latlon, dest_latlon, profile="driving"):
    """
    Consulta la API pública de OSRM para obtener una ruta entre dos puntos.

    Parámetros:
        origin_latlon: tupla (lat, lon) del punto de origen.
        dest_latlon: tupla (lat, lon) del punto de destino.
        profile: perfil de OSRM, por defecto "driving".

    Flujo:
        1. OSRM requiere el formato (lon, lat). Se reorganizan las coordenadas.
        2. Se construye la URL con parámetros que piden:
           - overview=full → ruta completa
           - geometries=geojson → lista de puntos
        3. Se hace la petición HTTP y se valida.
        4. Se extraen los puntos (en GeoJSON vienen como [lon, lat]).
        5. Se convierten a (lat, lon) para que Folium los entienda.

    Retorna:
        route_points: lista de coordenadas (lat, lon)
        distance: distancia total en metros
    """
    o_lon, o_lat = origin_latlon[1], origin_latlon[0]
    d_lon, d_lat = dest_latlon[1], dest_latlon[0]

    url = (
        f"http://router.project-osrm.org/route/v1/{profile}/"
        f"{o_lon},{o_lat};{d_lon},{d_lat}?overview=full&geometries=geojson"
    )

    resp = requests.get(url, timeout=20)
    resp.raise_for_status()  # Levanta excepción si la respuesta no es válida

    data = resp.json()

    # GeoJSON trae coordenadas como [lon, lat]; se invierte a (lat, lon)
    coords = data["routes"][0]["geometry"]["coordinates"]
    route_points = [(pt[1], pt[0]) for pt in coords]

    return route_points, data["routes"][0]["distance"]

def build_graph(route_points):
    """
    Construye un grafo dirigido que representa una ruta punto por punto.

    Cada nodo del grafo es un punto geográfico.
    Cada arista corresponde al segmento entre dos puntos consecutivos.

    Se usa geodesic() para calcular distancias reales entre puntos GPS.

    Este grafo puede servir para análisis como:
        - rutas alternativas
        - algoritmos de camino mínimo
        - simulaciones de transporte
    """
    G = nx.DiGraph()
    for i in range(len(route_points) - 1):
        p1, p2 = route_points[i], route_points[i + 1]
        dist_m = geodesic(p1, p2).meters  # Distancia en metros
        G.add_edge(p1, p2, weight=dist_m)
    return G

def build_map(fincas, destination, rutas, map_filename="rutas_fincas_centro.html"):
    """
    Construye un mapa interactivo (Folium) con:

    - Marcadores para cada finca.
    - Marcador para el centro de acopio.
    - Líneas representando rutas desde cada finca al destino.

    Parámetros:
        fincas: lista de diccionarios con info de cada finca.
        destination: tupla (lat, lon) del centro de acopio.
        rutas: diccionario con {nombre_finca: (lista_puntos, distancia_m)}.
        map_filename: nombre del archivo HTML de salida.

    Flujo:
        1. Se calcula un punto medio para centrar inicialmente el mapa.
        2. Se agregan marcadores de las fincas.
        3. Se agrega marcador del centro de acopio.
        4. Para cada ruta:
            - Se genera un color aleatorio.
            - Se dibuja un PolyLine con la ruta.
        5. Se ajusta el zoom automáticamente para ver todas las rutas.
        6. Se guarda el mapa.
    """

    # Punto medio aproximado para inicializar el mapa
    mid_lat = sum(f["lat"] for f in fincas) / len(fincas)
    mid_lon = sum(f["lon"] for f in fincas) / len(fincas)

    m = folium.Map(location=[mid_lat, mid_lon], zoom_start=7)

    # Agregar marcadores de fincas
    for finca in fincas:
        folium.Marker(
            location=(finca["lat"], finca["lon"]),
            tooltip=finca["nombre"],
            popup=finca["info"],
            icon=folium.Icon(color="green", icon="leaf"),
        ).add_to(m)

    # Agregar marcador del centro de acopio
    folium.Marker(
        destination,
        tooltip="Centro de Acopio",
        icon=folium.Icon(color="red", icon="home"),
    ).add_to(m)

    # Dibujar las rutas al centro de acopio
    for finca, (route_points, distance_m) in rutas.items():
        # Color aleatorio para diferenciar rutas
        color = "#%06x" % random.randint(0, 0xFFFFFF)
        folium.PolyLine(
            route_points,
            weight=5,
            opacity=0.7,
            color=color,
            tooltip=f"{finca}: {distance_m/1000:.2f} km",
        ).add_to(m)

    # Recalcular límites del mapa para incluir todos los puntos
    all_points = [p for ruta in rutas.values() for p in ruta[0]]

    sw = [min(p[0] for p in all_points), min(p[1] for p in all_points)]  # esquina inferior izquierda
    ne = [max(p[0] for p in all_points), max(p[1] for p in all_points)]  # esquina superior derecha

    m.fit_bounds([sw, ne])

    m.save(map_filename)
    return m


# Punto de entrada del script cuando se ejecuta directamente
if __name__ == "__main__":
    rutas = {}

    print("Generando rutas desde las fincas hasta el centro de acopio...\n")

    # Itera sobre cada finca y consulta la API OSRM
    for finca in fincas:
        origen = (finca["lat"], finca["lon"])
        try:
            # Obtiene los puntos y distancia de la ruta
            route_points, distance_m = get_osrm_route(origen, destination)
            rutas[finca["nombre"]] = (route_points, distance_m)

            print(f"{finca['nombre']}: {distance_m/1000:.2f} km ({len(route_points)} puntos)")
        except Exception as e:
            # Si la API falla, se reporta pero el script sigue con las demás fincas
            print(f"Error con {finca['nombre']}: {e}")

    # Construye y guarda el mapa final
    build_map(fincas, destination, rutas)
    print("\nMapa guardado como rutas_fincas_centro.html.")
