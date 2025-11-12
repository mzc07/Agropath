# rutas_unificadas.py
# Requisitos: pip install folium requests networkx geopy

import requests
import folium
import networkx as nx
from geopy.distance import geodesic
import random

# ======================================================
# 1. DATOS
# ======================================================

# Fincas
fincas = [
    {"nombre": "Finca 1", "lat": 40.92, "lon": -89.53, "info": "Parcela de producción"},
    {"nombre": "Finca 2", "lat": 40.92, "lon": -89.54, "info": "Parcela de producción"},
    {"nombre": "Finca 3", "lat": 40.91, "lon": -89.53, "info": "Parcela de producción"},
    {"nombre": "Finca 4", "lat": 40.91, "lon": -89.52, "info": "Parcela de producción"},
    {"nombre": "Finca 5", "lat": 40.91, "lon": -89.54, "info": "Parcela de producción"},
    {"nombre": "Finca 6", "lat": 40.91, "lon": -89.55, "info": "Parcela de producción"},
    {"nombre": "Finca 7", "lat": 40.91, "lon": -89.51, "info": "Parcela de producción"},
]

# Centro de acopio
centro_acopio = (39.481427, -88.303999)  # Clarkson Grain Mattoon Plant

# Destino adicional: Puerto de Metropolitan St. Louis
puerto = {
    "nombre": "Port of Metropolitan St. Louis",
    "lat": 38.61,
    "lon": -90.20,
    "info": (
        "Ubicación: Port of Metropolitan St. Louis\n"
        "Latitud: 38.61° N\nLongitud: 90.20° W\n"
        "Tipo: Puerto fluvial en el río Misisipi."
    ),
}

# ======================================================
# 2. FUNCIONES
# ======================================================

def get_osrm_route(origin_latlon, dest_latlon, profile="driving"):
    """Consulta OSRM y devuelve los puntos y la distancia total."""
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
    """Crea un grafo con pesos según distancias geodésicas."""
    G = nx.DiGraph()
    for i in range(len(route_points) - 1):
        p1, p2 = route_points[i], route_points[i + 1]
        dist_m = geodesic(p1, p2).meters
        G.add_edge(p1, p2, weight=dist_m)
    return G

def build_unified_map(fincas, centro_acopio, puerto, rutas, ruta_extra, map_filename="rutas_unificadas.html"):
    """Crea un único mapa con todas las rutas."""
    # Centro aproximado del mapa
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

    # Centro de acopio (Clarkson Grain Mattoon Plant)
    folium.Marker(
        centro_acopio,
        tooltip="Clarkson Grain Mattoon Plant",
        popup=(
            "<b>Clarkson Grain Mattoon Plant</b><br>"
            "Ubicación: Mattoon, Illinois<br>"
            "Latitud: 39.481427<br>"
            "Longitud: -88.303999<br>"
            "Tipo: Centro de acopio de granos."
        ),
        icon=folium.Icon(color="red", icon="home"),
    ).add_to(m)

    # Puerto de Metropolitan St. Louis
    folium.Marker(
        location=(puerto["lat"], puerto["lon"]),
        tooltip=puerto["nombre"],
        popup=f"<b>{puerto['nombre']}</b><br>{puerto['info'].replace(chr(10), '<br>')}",
        icon=folium.Icon(color="blue", icon="anchor"),
    ).add_to(m)

    # Rutas de fincas → centro
    for finca, (route_points, distance_m) in rutas.items():
        color = "#%06x" % random.randint(0, 0xFFFFFF)
        folium.PolyLine(
            route_points,
            weight=4,
            opacity=0.8,
            color=color,
            tooltip=f"{finca}: {distance_m/1000:.2f} km",
        ).add_to(m)

    # Ruta del centro de acopio → puerto
    if ruta_extra:
        route_points, distance_m = ruta_extra
        folium.PolyLine(
            route_points,
            weight=6,
            opacity=0.8,
            color="blue",
            tooltip=f"Centro → Puerto: {distance_m/1000:.2f} km",
        ).add_to(m)

    # Ajustar vista
    all_points = [p for ruta in rutas.values() for p in ruta[0]]
    if ruta_extra:
        all_points += ruta_extra[0]
    sw = [min(p[0] for p in all_points), min(p[1] for p in all_points)]
    ne = [max(p[0] for p in all_points), max(p[1] for p in all_points)]
    m.fit_bounds([sw, ne])

    m.save(map_filename)
    return m

# ======================================================
# 3. PROCESO PRINCIPAL
# ======================================================

if __name__ == "__main__":
    rutas = {}

    print("\nGenerando rutas de fincas → centro de acopio...\n")
    for finca in fincas:
        origen = (finca["lat"], finca["lon"])
        try:
            route_points, distance_m = get_osrm_route(origen, centro_acopio)
            rutas[finca["nombre"]] = (route_points, distance_m)
            print(f"{finca['nombre']}: {distance_m/1000:.2f} km ({len(route_points)} puntos)")
        except Exception as e:
            print(f"Error con {finca['nombre']}: {e}")

    # Ruta del centro al puerto
    print("\nGenerando ruta centro de acopio → puerto...\n")
    ruta_extra = None
    try:
        route_points_extra, distance_extra = get_osrm_route(centro_acopio, (puerto["lat"], puerto["lon"]))
        ruta_extra = (route_points_extra, distance_extra)
        print(f"Centro → Puerto: {distance_extra/1000:.2f} km ({len(route_points_extra)} puntos)")
    except Exception as e:
        print(f"Error en ruta adicional: {e}")

    # Construcción del grafo total
    G_total = nx.DiGraph()
    for finca, (ruta, _) in rutas.items():
        G_total.update(build_graph(ruta))
    if ruta_extra:
        G_total.update(build_graph(ruta_extra[0]))

    print(f"\nGrafo total: {G_total.number_of_nodes()} nodos, {G_total.number_of_edges()} aristas.")
    total_weight = sum(nx.get_edge_attributes(G_total, "weight").values())
    print(f"Peso total del grafo: {total_weight/1000:.2f} km")

    # Crear mapa unificado
    build_unified_map(fincas, centro_acopio, puerto, rutas, ruta_extra)
    print("\nMapa guardado como rutas_unificadas.html.")

