# ruta_folium_osrm_networkx.py
# Requisitos: pip install folium requests networkx geopy
#
# Este script:
# 1. Consulta OSRM para obtener una ruta entre dos coordenadas.
# 2. Convierte los puntos de la ruta en un grafo dirigido usando NetworkX.
# 3. Calcula distancias con geodesic.
# 4. Visualiza la ruta en un mapa interactivo con Folium.
# 5. Calcula la ruta más corta dentro del propio grafo reconstruido.

import requests
import folium
import networkx as nx
from geopy.distance import geodesic

# Coordenadas iniciales (latitud, longitud)
# Estas representan el origen y destino para solicitar la ruta a OSRM.
origin = (39.481427, -88.303999)
destination = (38.61, -90.20)

def get_osrm_route(origin_latlon, dest_latlon, profile="driving"):
    """
    Consulta la API pública de OSRM para obtener la geometría completa
    de la ruta entre dos puntos.

    Parámetros:
        origin_latlon: (lat, lon) del origen.
        dest_latlon: (lat, lon) del destino.
        profile: modo de transporte ("driving", "walking", "cycling").

    Retorna:
        route_points: lista de tuplas (lat, lon) con cada punto de la ruta.
        distance_m: distancia total en metros según OSRM.
    """

    # OSRM requiere formato lon,lat (invertido respecto a folium/geopy)
    o_lon, o_lat = origin_latlon[1], origin_latlon[0]
    d_lon, d_lat = dest_latlon[1], dest_latlon[0]

    # URL hacia el servidor público OSRM con parámetros para obtener la geometría en GeoJSON
    url = (
        f"http://router.project-osrm.org/route/v1/{profile}/"
        f"{o_lon},{o_lat};{d_lon},{d_lat}?overview=full&geometries=geojson"
    )

    # Petición HTTP con timeout para evitar cuelgues
    resp = requests.get(url, timeout=20)
    resp.raise_for_status()  # Lanza error si falla

    data = resp.json()

    # La geometría viene como una lista de [lon, lat]
    coords = data["routes"][0]["geometry"]["coordinates"]

    # Convertimos cada punto a (lat, lon) para usar en geopy/folium
    route_points = [(pt[1], pt[0]) for pt in coords]

    return route_points, data["routes"][0]["distance"]

def build_graph(route_points):
    """
    Crea un grafo dirigido donde cada punto de la ruta es un nodo
    y cada tramo consecutivo es una arista con peso igual a la
    distancia geodésica (en metros).

    Esto permite usar algoritmos de rutas como Dijkstra o A* directamente
    sobre la ruta obtenida de OSRM.
    """
    G = nx.DiGraph()

    # Recorre cada par consecutivo de puntos y calcula distancia geodésica.
    for i in range(len(route_points) - 1):
        p1, p2 = route_points[i], route_points[i + 1]

        # Distancia en metros entre p1 y p2
        dist_m = geodesic(p1, p2).meters

        # El grafo es dirigido porque la ruta tiene dirección implícita.
        G.add_edge(p1, p2, weight=dist_m)

    return G

def build_map(origin, destination, route_points, map_filename="ruta_osrm.html"):
    """
    Construye un mapa interactivo con Folium:
    - Marca origen y destino.
    - Dibuja la línea de la ruta.
    - Ajusta el mapa a los límites de la ruta.
    - Guarda el archivo HTML.

    Retorna:
        Un objeto folium.Map.
    """

    # Punto medio aproximado para centrar el mapa inicialmente
    mid_lat = (origin[0] + destination[0]) / 2
    mid_lon = (origin[1] + destination[1]) / 2

    m = folium.Map(location=[mid_lat, mid_lon], zoom_start=8)

    # Marcadores básicos
    folium.Marker(origin, tooltip="Origen").add_to(m)
    folium.Marker(destination, tooltip="Destino").add_to(m)

    # Línea de la ruta
    folium.PolyLine(route_points, weight=6, opacity=0.8, color="blue").add_to(m)

    # Calcular límites del recorrido para ajustar vista automáticamente
    sw = [min(p[0] for p in route_points), min(p[1] for p in route_points)]
    ne = [max(p[0] for p in route_points), max(p[1] for p in route_points)]
    m.fit_bounds([sw, ne])

    m.save(map_filename)
    return m

def generar_ruta_cent():
    # Obtener la ruta desde OSRM
    route_points, distance_m = get_osrm_route(origin, destination)
    print(f"Ruta total: {distance_m/1000:.2f} km con {len(route_points)} puntos.")

    # Construir grafo con la ruta
    G = build_graph(route_points)
    print(f"Grafo construido con {G.number_of_nodes()} nodos y {G.number_of_edges()} aristas.")

    # Calcular la suma de pesos (debería ser muy similar a la distancia OSRM)
    total_weight = sum(nx.get_edge_attributes(G, "weight").values())
    print(f"Peso total del grafo (suma de distancias): {total_weight/1000:.2f} km")

    # Ejemplo: ruta más corta usando Dijkstra sobre el grafo construido
    shortest_path = nx.shortest_path(
        G,
        source=route_points[0],
        target=route_points[-1],
        weight="weight"
    )
    path_len = nx.shortest_path_length(
        G,
        source=route_points[0],
        target=route_points[-1],
        weight="weight"
    )

    print(f"Ruta más corta en el grafo: {len(shortest_path)} nodos, {path_len/1000:.2f} km")

    # Crear y guardar el mapa HTML
    build_map(origin, destination, route_points)
    print("Mapa guardado como ruta_osrm.html.")
