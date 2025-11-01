import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import tkinter as tk
from tkinter import messagebox

centros = [
    {"nombre": "LaSalle", "lat": 41.3339, "lon": -89.0911,
     "info": "Condado de LaSalle, Illinois.\nImportante región agrícola."},
    {"nombre": "Iroquois", "lat": 40.7453, "lon": -87.8251,
     "info": "Condado de Iroquois, Illinois.\nProducción destacada de maíz y soya."},
    {"nombre": "McLean", "lat": 40.4931, "lon": -88.8454,
     "info": "Condado de McLean, Illinois.\nUno de los mayores productores de granos."}
]

def mostrar_info(nombre, info):
    ventana_raiz = tk.Tk()
    ventana_raiz.withdraw()
    messagebox.showinfo(nombre, info)
    ventana_raiz.destroy()

def click_event(event):
    if not event.inaxes:
        return
    for c in centros:
        dx = abs(event.xdata - c["lon"])
        dy = abs(event.ydata - c["lat"])
        if dx < 0.15 and dy < 0.15:  # tolerancia
            mostrar_info(c["nombre"], c["info"])
            break

def ver_fincas():
    fig = plt.figure(figsize=(6,6))
    ax = plt.axes(projection=ccrs.PlateCarree())

    ax.set_extent([-91.6, -87.4, 36.9, 42.5])
    ax.add_feature(cfeature.STATES.with_scale('10m'), edgecolor='black')
    ax.add_feature(cfeature.BORDERS.with_scale('10m'))
    ax.add_feature(cfeature.LAND)
    ax.add_feature(cfeature.LAKES, color='lightblue')

    for c in centros:
        ax.plot(c["lon"], c["lat"], marker='o', color='red', markersize=6, transform=ccrs.PlateCarree())
        ax.text(c["lon"] + 0.05, c["lat"] + 0.05, c["nombre"],
                transform=ccrs.PlateCarree(), fontsize=8, color='red')

    plt.title('Illinois - Fincas')
    fig.canvas.mpl_connect("button_press_event", click_event)
    plt.show()