import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import tkinter as tk
from tkinter import messagebox

# Lista de fincas
fincas = [
    {"nombre": "Finca 1", "lat": 40.92, "lon": -89.53, "info": "Parcela de producción"},
    {"nombre": "Finca 2", "lat": 40.92, "lon": -89.54, "info": "Parcela de producción"},
    {"nombre": "Finca 3", "lat": 40.91, "lon": -89.53, "info": "Parcela de producción"},
    {"nombre": "Finca 4", "lat": 40.91, "lon": -89.52, "info": "Parcela de producción"},
    {"nombre": "Finca 5", "lat": 40.91, "lon": -89.54, "info": "Parcela de producción"},
    {"nombre": "Finca 6", "lat": 40.91, "lon": -89.55, "info": "Parcela de producción"},
    {"nombre": "Finca 7", "lat": 40.91, "lon": -89.51, "info": "Parcela de producción"},
]

def mostrar_info(nombre, info):
    ventana_raiz = tk.Tk()
    ventana_raiz.withdraw()
    messagebox.showinfo(nombre, info)
    ventana_raiz.destroy()

def click_event(event):
    if not event.inaxes:
        return
    for f in fincas:
        dx = abs(event.xdata - f["lon"])
        dy = abs(event.ydata - f["lat"])
        if dx < 0.01 and dy < 0.01:  # tolerancia más precisa
            mostrar_info(f["nombre"], f["info"])
            break

def ver_fincas():
    fig = plt.figure(figsize=(6,6))
    ax = plt.axes(projection=ccrs.PlateCarree())

    # Zoom ajustado a fincas
    ax.set_extent([-89.57, -89.49, 40.89, 40.94])

    # Agregar elementos del mapa
    ax.add_feature(cfeature.STATES.with_scale('10m'), edgecolor='black')
    ax.add_feature(cfeature.BORDERS.with_scale('10m'))
    ax.add_feature(cfeature.LAND)
    ax.add_feature(cfeature.LAKES, color='lightblue')

    # Dibujar fincas
    for f in fincas:
        ax.plot(f["lon"], f["lat"], marker='o', color='blue', markersize=6, transform=ccrs.PlateCarree())
        ax.text(f["lon"] + 0.005, f["lat"] + 0.005, f["nombre"],
                transform=ccrs.PlateCarree(), fontsize=8, color='blue')

    plt.title('Mapa de Fincas - Parcela de producción')
    fig.canvas.mpl_connect("button_press_event", click_event)
    plt.show()

