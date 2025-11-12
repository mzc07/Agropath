# ruta_folium_osrm_networkx.py
# Requisitos: pip install folium requests networkx geopy

import requests
import folium
import networkx as nx
from geopy.distance import geodesic

# Coordenadas iniciales
origin = (39.481427, -88.303999)
destination = (38.61, -90.20)

def get_osrm_route(origin_latlon, dest_latlon, profile="driving"):
    o_lon, o_lat = origin_latlon[1], origin_latlon[0]
    d_lon, d_lat = dest_latlon[1], dest_latlon[0]
    url = (
        f"http://router.project-osrm.org/route/v1/{profile}/"
        f"{o_lon},{o_lat};{d_lon},{d_lat}?overview=full&geometries=geojson"
    )
    resp = requests.get(url, timeout=20)
    resp.raise_for_status()
    data = resp.json()
    coords = data["routes"][0]["geometry"]["coordinates"]
    route_points = [(pt[1], pt[0]) for pt in coords]
    return route_points, data["routes"][0]["distance"]

def build_graph(route_points):
    """
    Crea un grafo dirigido con pesos basados en la distancia geodésica (metros)
    entre puntos consecutivos de la ruta.
    """
    G = nx.DiGraph()
    for i in range(len(route_points) - 1):
        p1, p2 = route_points[i], route_points[i + 1]
        dist_m = geodesic(p1, p2).meters
        G.add_edge(p1, p2, weight=dist_m)
    return G

def build_map(origin, destination, route_points, map_filename="ruta_osrm.html"):
    mid_lat = (origin[0] + destination[0]) / 2
    mid_lon = (origin[1] + destination[1]) / 2
    m = folium.Map(location=[mid_lat, mid_lon], zoom_start=8)
    folium.Marker(origin, tooltip="Origen").add_to(m)
    folium.Marker(destination, tooltip="Destino").add_to(m)
    folium.PolyLine(route_points, weight=6, opacity=0.8, color="blue").add_to(m)
    sw = [min(p[0] for p in route_points), min(p[1] for p in route_points)]
    ne = [max(p[0] for p in route_points), max(p[1] for p in route_points)]
    m.fit_bounds([sw, ne])
    m.save(map_filename)
    return m

if __name__ == "__main__":
    route_points, distance_m = get_osrm_route(origin, destination)
    print(f"Ruta total: {distance_m/1000:.2f} km con {len(route_points)} puntos.")

    G = build_graph(route_points)
    print(f"Grafo construido con {G.number_of_nodes()} nodos y {G.number_of_edges()} aristas.")
    total_weight = sum(nx.get_edge_attributes(G, "weight").values())
    print(f"Peso total del grafo (suma de distancias): {total_weight/1000:.2f} km")

    # Ejemplo: calcular la ruta más corta entre origen y destino según el grafo (Dijkstra)
    shortest_path = nx.shortest_path(G, source=route_points[0], target=route_points[-1], weight="weight")
    path_len = nx.shortest_path_length(G, source=route_points[0], target=route_points[-1], weight="weight")
    print(f"Ruta más corta en el grafo: {len(shortest_path)} nodos, {path_len/1000:.2f} km")

    # Crear mapa
    build_map(origin, destination, route_points)
    print("Mapa guardado como ruta_osrm.html.")
