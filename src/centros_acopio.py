import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import tkinter as tk
from tkinter import messagebox

lat, lon = 39.481427, -88.303999

def mostrar_info():
    ventana_raiz = tk.Tk()
    ventana_raiz.withdraw()
    messagebox.showinfo("Clarkson Grain Mattoon Plant",
                        "Ubicación: Mattoon, Illinois\n"
                        "Latitud: 39.481427\nLongitud: -88.303999\n"
                        "Tipo: Centro de acopio de granos.")
    ventana_raiz.destroy()

def click_event(event):
    if event.inaxes:
        dx = abs(event.xdata - lon)
        dy = abs(event.ydata - lat)
        if dx < 0.1 and dy < 0.1:
            mostrar_info()

def ver_centrosacopio():
    fig = plt.figure(figsize=(6,6))
    ax = plt.axes(projection=ccrs.PlateCarree())

    ax.set_extent([-91.6, -87.4, 36.9, 42.5])
    ax.add_feature(cfeature.STATES.with_scale('10m'), edgecolor='black')
    ax.add_feature(cfeature.BORDERS.with_scale('10m'))
    ax.add_feature(cfeature.LAND)
    ax.add_feature(cfeature.LAKES, color='lightblue')

    ax.plot(lon, lat, marker='o', color='red', markersize=6, transform=ccrs.PlateCarree())
    ax.text(lon + 0.05, lat + 0.05, 'Clarkson Grain Mattoon Plant',
            transform=ccrs.PlateCarree(), fontsize=8, color='red')

    plt.title('Illinois - Centros de acopio')

    fig.canvas.mpl_connect("button_press_event", click_event)
    plt.show()