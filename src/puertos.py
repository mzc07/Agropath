import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt

def ver_puertos():
    plt.figure(figsize=(6,6))
    ax = plt.axes(projection=ccrs.PlateCarree())

    ax.set_extent([-91.6, -87.4, 36.9, 42.5])

    ax.add_feature(cfeature.STATES.with_scale('10m'), edgecolor='black')
    ax.add_feature(cfeature.BORDERS.with_scale('10m'))
    ax.add_feature(cfeature.LAND)
    ax.add_feature(cfeature.LAKES, color='lightblue')

    plt.title('Illinois - Centros de acopio')
    plt.show()
