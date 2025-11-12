# rutas_fincas_centro_acopio.py
# Requisitos: pip install folium requests networkx geopy

import requests
import folium
import networkx as nx
from geopy.distance import geodesic
import random

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

# Centro de acopio (destino)
destination = (39.481427, -88.303999)  # Clarkson Grain Mattoon Plant (lat, lon)

def get_osrm_route(origin_latlon, dest_latlon, profile="driving"):
    """Consulta la API pública de OSRM y devuelve los puntos de la ruta y la distancia total."""
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
    """Crea un grafo dirigido con pesos basados en la distancia geodésica entre puntos consecutivos."""
    G = nx.DiGraph()
    for i in range(len(route_points) - 1):
        p1, p2 = route_points[i], route_points[i + 1]
        dist_m = geodesic(p1, p2).meters
        G.add_edge(p1, p2, weight=dist_m)
    return G

def build_map(fincas, destination, rutas, map_filename="rutas_fincas_centro.html"):
    """Construye un mapa Folium con todas las rutas de las fincas al centro de acopio."""
    mid_lat = sum(f["lat"] for f in fincas) / len(fincas)
    mid_lon = sum(f["lon"] for f in fincas) / len(fincas)
    m = folium.Map(location=[mid_lat, mid_lon], zoom_start=7)

    # Marcadores de fincas
    for finca in fincas:
        folium.Marker(
            location=(finca["lat"], finca["lon"]),
            tooltip=finca["nombre"],
            popup=finca["info"],
            icon=folium.Icon(color="green", icon="leaf"),
        ).add_to(m)

    # Marcador del centro de acopio
    folium.Marker(
        destination,
        tooltip="Centro de Acopio",
        icon=folium.Icon(color="red", icon="home"),
    ).add_to(m)

    # Rutas desde cada finca
    for finca, (route_points, distance_m) in rutas.items():
        color = "#%06x" % random.randint(0, 0xFFFFFF)
        folium.PolyLine(
            route_points,
            weight=5,
            opacity=0.7,
            color=color,
            tooltip=f"{finca}: {distance_m/1000:.2f} km",
        ).add_to(m)

    # Ajustar vista
    all_points = [p for ruta in rutas.values() for p in ruta[0]]
    sw = [min(p[0] for p in all_points), min(p[1] for p in all_points)]
    ne = [max(p[0] for p in all_points), max(p[1] for p in all_points)]
    m.fit_bounds([sw, ne])

    m.save(map_filename)
    return m

if __name__ == "__main__":
    rutas = {}

    print("Generando rutas desde las fincas hasta el centro de acopio...\n")
    for finca in fincas:
        origen = (finca["lat"], finca["lon"])
        try:
            route_points, distance_m = get_osrm_route(origen, destination)
            rutas[finca["nombre"]] = (route_points, distance_m)
            print(f"{finca['nombre']}: {distance_m/1000:.2f} km ({len(route_points)} puntos)")
        except Exception as e:
            print(f"Error con {finca['nombre']}: {e}")

    build_map(fincas, destination, rutas)
    print("\nMapa guardado como rutas_fincas_centro.html.")

