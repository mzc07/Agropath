import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import tkinter as tk
from tkinter import messagebox

lat, lon = 38.61, -90.20

def mostrar_info():
    ventana_raiz = tk.Tk()
    ventana_raiz.withdraw()
    messagebox.showinfo(
        "Port of Metropolitan St. Louis",
        "Ubicación: Port of Metropolitan St. Louis\n"
        "Latitud: 38.61° N\nLongitud: 90.20° W\n"
        "Tipo: Puerto fluvial en el río Misisipi."
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

    ax.set_extent([-92, -88, 37, 40])
    ax.add_feature(cfeature.STATES.with_scale('10m'), edgecolor='black')
    ax.add_feature(cfeature.BORDERS.with_scale('10m'))
    ax.add_feature(cfeature.LAND)
    ax.add_feature(cfeature.LAKES, color='lightblue')
    ax.add_feature(cfeature.COASTLINE)

    ax.plot(lon, lat, marker='o', color='red', markersize=6, transform=ccrs.PlateCarree())
    ax.text(lon + 0.1, lat + 0.1, 'Port of Metropolitan St. Louis',
            transform=ccrs.PlateCarree(), fontsize=8, color='red')

    plt.title('Port of Metropolitan St. Louis - 38.61° N, 90.20° W')

    fig.canvas.mpl_connect("button_press_event", click_event)
    plt.show()