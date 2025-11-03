import osmnx as ox
import networkx as nx
from statistics import mean

fincas = [
    {"nombre": "Finca 1", "lat": 40.92, "lon": -89.53},
    {"nombre": "Finca 2", "lat": 40.92, "lon": -89.54},
    {"nombre": "Finca 3", "lat": 40.91, "lon": -89.53},
    {"nombre": "Finca 4", "lat": 40.91, "lon": -89.52},
    {"nombre": "Finca 5", "lat": 40.91, "lon": -89.54},
    {"nombre": "Finca 6", "lat": 40.91, "lon": -89.55},
    {"nombre": "Finca 7", "lat": 40.91, "lon": -89.51},
]

centro = {"lat": 39.481427, "lon": -88.303999}

# ---------------- 1. Centroide del área ----------------
lat_centro = mean([f["lat"] for f in fincas] + [centro["lat"]])
lon_centro = mean([f["lon"] for f in fincas] + [centro["lon"]])

# Radio = distancia aproximada más lejana desde el centroide al centro de acopio
# Aquí usamos 120 km como radio de descarga del grafo
radio_m = 120_000  

G = ox.graph_from_point(
    center_point=(lat_centro, lon_centro),
    dist=radio_m,
    network_type='drive'
)

G = ox.add_edge_speeds(G)
G = ox.add_edge_travel_times(G)

# ---------------- 2. Convertir lat/lon a nodos ----------------
for finca in fincas:
    finca["nodo"] = ox.distance.nearest_nodes(G, X=finca["lon"], Y=finca["lat"])

centro["nodo"] = ox.distance.nearest_nodes(G, X=centro["lon"], Y=centro["lat"])

# ---------------- 3. Rutas más rápidas ----------------
rutas = []
for finca in fincas:
    ruta = nx.shortest_path(G, finca["nodo"], centro["nodo"], weight="travel_time")
    distancia = nx.shortest_path_length(G, finca["nodo"], centro["nodo"], weight="length")
    tiempo = nx.shortest_path_length(G, finca["nodo"], centro["nodo"], weight="travel_time")

    rutas.append({
        "finca": finca["nombre"],
        "distancia_km": round(distancia / 1000, 2),
        "tiempo_min": round(tiempo / 60, 2),
        "nodos": len(ruta)
    })

# ---------------- 4. Imprimir resultados ----------------
for r in rutas:
    print(f"{r['finca']} -> Centro de acopio:")
    print(f"   Distancia: {r['distancia_km']} km")
    print(f"   Tiempo estimado: {r['tiempo_min']} min")
    print(f"   Pasos en ruta: {r['nodos']}\n")
