#### SCRIPT PARA GRAFICAR UN CAMPO LAT LON DE ALGUNA VARIABLE DE LA SALIDA DEL WRF V4.0                   ####
#### ADAPTADO DE https://wrf-python.readthedocs.io/en/latest/plot.html                                    ####
#### POWERED BY HUAYRA-TORO                                                                               ####
#### INFO SOBRE LAS VARIABLES DE DIAGNOSTICO https://wrf-python.readthedocs.io/en/latest/diagnostics.html #### 
#### GRAFICA OMEGA                                                                                        ####
from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap
import cartopy.crs as crs
from cartopy.feature import NaturalEarthFeature
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import cartopy.feature as cfeature
from datetime import datetime, timedelta
import scipy.ndimage as ndimage
from wrf import (getvar, interplevel, to_np, latlon_coords, get_cartopy,
                 cartopy_xlim, cartopy_ylim, ALL_TIMES)

states_provinces = cfeature.NaturalEarthFeature(
        category='cultural',
        name='admin_1_states_provinces_lines',
        scale='10m',
        facecolor='none',edgecolor='black')

countries = cfeature.NaturalEarthFeature(
        category='cultural',
        name='admin_0_countries',
        scale='10m',
        facecolor='none',edgecolor='black')

## SE CARGA LA SALIDA SIN POSTPROCESAR
wrf_file = Dataset("...")
## cantidad de tiempos
tpos = (getvar(wrf_file, "z", ALL_TIMES).shape)[0]

# agregar el inicio de la corrida, y luego ver el espaciado de cada una
t_ini = datetime.strptime('17-09-2012 18:00:00', '%d-%m-%Y %H:%M:%S')

############# ESPECIFICAR EL CAMPO DE PRESION QUE SE QUIERA #############

nivel = 700 

# SE EXTRAEN LAS VARIABLES A UTILIZAR
# SE HACE UN CICLO PARA TODOS LOS TIEMPOS DEL WRF_FILE

for tidx in range(0, tpos) :       # len(tpos)  
        p = getvar(wrf_file, "pressure", tidx)  # presion
        z = getvar(wrf_file, "z", tidx, units = 'm')     # geopotencial
        w = getvar(wrf_file, "wa", tidx, units="m s-1")   # vel vertical
        ter = getvar(wrf_file, "ter", tidx)     # terreno alturas

        # Se interpolan las variables al campo de presion correspondiente para podee graficarlas 
        w = interplevel(w, p, nivel)

        # Se extraen lat-lon
        lats, lons = latlon_coords(p)

        # Se extrae info de la proyeccion 
        cart_proj = get_cartopy(p)
        
############################################## GRAFICADO ############################################## 
        
        fig = plt.figure(figsize=(12,9))
        ax = plt.axes(projection=cart_proj)

        # Aniadiendo los sombreados
        #levels = [25, 30, 35, 40, 50, 60, 70, 80, 90, 100, 110, 120]
        levels = np.arange(-1.5, 1.5, 0.25)
        wspd_contours = plt.contourf(to_np(lons), to_np(lats), to_np(w),
                             levels=levels,
                             cmap="bwr",
                             transform=crs.PlateCarree())
        plt.colorbar(wspd_contours, ax=ax)
        
        ht_fill = plt.contourf(to_np(lons), to_np(lats), to_np(ter), np.arange(3000, 9000, 100),colors=['saddlebrown'], transform=crs.PlateCarree())
        
        # Set the map bounds
        ax.set_xlim(cartopy_xlim(p))
        ax.set_ylim(cartopy_ylim(p))

        # Agregamos la línea de costas
        ax.coastlines(resolution='10m',linewidth=0.6)
        # Agregamos los límites de los países
        ax.add_feature(countries,linewidth=0.9)
        # Agregamos los límites de las provincias
        ax.add_feature(states_provinces,linewidth=0.9)
        # Le damos formato a las etiquetas de los ticks
        ax.set_yticks(np.arange(-29, -19, 2), crs=crs.PlateCarree())
        ax.set_xticks(np.arange(-70, -59, 2), crs=crs.PlateCarree())
        lon_formatter = LongitudeFormatter(zero_direction_label=True)
        lat_formatter = LatitudeFormatter()
        ax.xaxis.set_major_formatter(lon_formatter)
        ax.yaxis.set_major_formatter(lat_formatter)
        # para escribir el titulo
        if tidx == 0 :
                dd = 0
                plt.title("Velocidad vertical en 700 hPa (m s-1) en " + str((t_ini)))
                plt.show()
                continue
        if tidx > 0 :
                dd = dd + 3 
                plt.title("Velocidad vertical en 700 hPa (m s-1) en " + str((t_ini+timedelta(hours=dd))))
                plt.show()

