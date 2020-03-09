#################################################################################
## SCRIPT PARA HACER CORTES VERTICALES CON TERRENO EN LAS SALIDAS DEL WRF V4.0 ##
## ADAPTADO DE https://wrf-python.readthedocs.io/en/latest/plot.html ##
## POWERED BY HUARYRA-TORO ##

import numpy as np
from matplotlib import pyplot
from matplotlib.cm import get_cmap
from matplotlib.colors import from_levels_and_colors
from cartopy import crs
from cartopy.feature import NaturalEarthFeature, COLORS
from netCDF4 import Dataset
from wrf import (getvar, to_np, get_cartopy, latlon_coords, vertcross,cartopy_xlim, cartopy_ylim, interpline, CoordPair, ALL_TIMES)

## SE CARGA LA SALIDA SIN POSTPROCESAR
wrf_file = Dataset("...")

## PARA SABER LAS VARIABLES Q CONTIENE EL NETCDF
#print(wrf_file.variables.keys())

# Definir lat y lon del corte vertical
cross_start = CoordPair(lat=-24.75, lon=-68.5)
cross_end = CoordPair(lat=-24.75, lon=-62)

# Se consiguen las variables del WRF
tidx = 0        ## es el tiempo de la corrida, desde cero hasta el tiempo final
## PARA TERRENO
ht = getvar(wrf_file, "z", tidx)
ter = getvar(wrf_file, "ter", tidx)
## VARIABLE PARA GRAFICAR 
var = getvar(wrf_file, "rh", tidx)

# Se hace la interpolacion de la variable con el terreno

var_cross = vertcross(var, ht, wrfin=wrf_file,
                    start_point=cross_start,
                    end_point=cross_end,
                    latlon=True, meta=True)

# Para agregar los atributos a la variable (opcional) 
#var_cross.attrs.update(var_cross.attrs)
#var_cross.attrs["description"] = "radar reflectivity cross section"
#var_cross.attrs["units"] = "dBZ"

# Se hace un interpolado entre los valores 
# proximos a la topografia y los NaN para que
# quede mas lindo el grafico XD.
var_cross_filled = np.ma.copy(to_np(var_cross))

for i in range(var_cross_filled.shape[-1]):
    column_vals = var_cross_filled[:,i]
    first_idx = int(np.transpose((column_vals > -200).nonzero())[0])
    var_cross_filled[0:first_idx, i] = var_cross_filled[first_idx, i]

# Para sacar las alturas del terreno del corte
ter_line = interpline(ter, wrfin=wrf_file, start_point=cross_start,
                      end_point=cross_end)

# Sacar las lat/lon
lats, lons = latlon_coords(var)

# Sacar la projeccion de cartopy
cart_proj = get_cartopy(var)

############# GRAFICADO ############# 
# Figura
fig = pyplot.figure(figsize=(8,6))
ax_cross = pyplot.axes()

## si se quiere tener un intervalo para los datos 
var_levels = np.arange(5, 100., 10.)

# Se hace el grafico de la variable 
xs = np.arange(0, var_cross.shape[-1], 1)
ys = to_np(var_cross.coords["vertical"])
dbz_contours = ax_cross.contourf(xs,
                                 ys,
                                 to_np(var_cross_filled),
                                 cmap='bwr',
                                 extend="both")
# Se agrega la colorbar
cb_dbz = fig.colorbar(dbz_contours, ax=ax_cross)
cb_dbz.ax.tick_params(labelsize=8)

# Se enmascara la montania con color marron (se cambia en facecolor) 
ht_fill = ax_cross.fill_between(xs, 0, to_np(ter_line),
                                facecolor="saddlebrown")

# Para agregar los ejes de coordenadas en el versor x
coord_pairs = to_np(var_cross.coords["xy_loc"])
x_ticks = np.arange(coord_pairs.shape[0])
x_labels = [pair.latlon_str() for pair in to_np(coord_pairs)]

# 
num_ticks = 7
thin = int((len(x_ticks) / num_ticks) + .5)
ax_cross.set_xticks(x_ticks[::thin])
ax_cross.set_xticklabels(x_labels[::thin], rotation=45, fontsize=8)

# Se agrega el nombre del eje y
ax_cross.set_ylabel("Altura (m)", fontsize=12)

# Se agrega un titulo
ax_cross.set_title("Corte vertical de ...", {"fontsize" : 14})

pyplot.show()
