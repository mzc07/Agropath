import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import tkinter as tk
from tkinter import messagebox

lat, lon = 46.0104, -122.8424

def mostrar_info():
    ventana_raiz = tk.Tk()
    ventana_raiz.withdraw()
    messagebox.showinfo(
        "Port of Kalama",
        "Ubicación: Kalama, Washington\n"
        "Latitud: 46.0104\nLongitud: -122.8424\n"
        "Tipo: Puerto industrial y de carga."
    )
    ventana_raiz.destroy()

def click_event(event):
    if event.inaxes:
        dx = abs(event.xdata - lon)
        dy = abs(event.ydata - lat)
        if dx < 0.1 and dy < 0.1:
            mostrar_info()

def ver_puertos():
    fig = plt.figure(figsize=(6,6))
    ax = plt.axes(projection=ccrs.PlateCarree())

    ax.set_extent([-124, -121, 45.5, 47.5])
    ax.add_feature(cfeature.STATES.with_scale('10m'), edgecolor='black')
    ax.add_feature(cfeature.BORDERS.with_scale('10m'))
    ax.add_feature(cfeature.LAND)
    ax.add_feature(cfeature.LAKES, color='lightblue')
    ax.add_feature(cfeature.COASTLINE)

    # Punto del puerto
    ax.plot(lon, lat, marker='o', color='red', markersize=6, transform=ccrs.PlateCarree())
    ax.text(lon + 0.05, lat + 0.05, 'Port of Kalama',
            transform=ccrs.PlateCarree(), fontsize=8, color='red')

    plt.title('Washington - Port of Kalama')

    fig.canvas.mpl_connect("button_press_event", click_event)
    plt.show()
