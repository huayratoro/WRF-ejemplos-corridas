import numpy as np
import matplotlib.pyplot as plt 
from matplotlib.cm import get_cmap
from matplotlib.colors import from_levels_and_colors
from cartopy import crs
from cartopy.feature import NaturalEarthFeature, COLORS
from netCDF4 import Dataset
from wrf import (getvar, to_np, get_cartopy, latlon_coords, vertcross,cartopy_xlim, cartopy_ylim, interpline, CoordPair, ALL_TIMES)
from datetime import datetime, timedelta

## SE CARGA LA SALIDA SIN POSTPROCESAR
wrf_file = Dataset("...")
## cantidad de tiempos
tpos = (getvar(wrf_file, "z", ALL_TIMES).shape)[0]

# agregar el inicio de la corrida, y luego ver el espaciado de cada una
t_ini = datetime.strptime('17-09-2012 18:00:00', '%d-%m-%Y %H:%M:%S')

# Definir lat y lon del corte vertical
cross_start = CoordPair(lat=-24.75, lon=-68.5)
cross_end = CoordPair(lat=-24.75, lon=-62)

if tpos == 0 : 
        print('ES UN SOLO TPO')
        exit()
# Se consiguen las variables del WRF
for tidx in range(0,tpos) :
#tidx = 8        ## es el tiempo de la corrida, desde cero hasta el tiempo final
        ## PARA TERRENO
        ht = getvar(wrf_file, "z", tidx)
        ter = getvar(wrf_file, "ter", tidx)
        w = getvar(wrf_file, 'wa', tidx)
        ## VARIABLE PARA GRAFICAR 
        ## Una lista de variables : https://wrf-python.readthedocs.io/en/latest/user_api/generated/wrf.getvar.html#wrf.getvar
        var = getvar(wrf_file, "theta", tidx)
        cmap = 'seismic'
        # Se hace la interpolacion de la variable con el terreno
        var_cross = vertcross(var, ht, wrfin=wrf_file,
                            start_point=cross_start,
                            end_point=cross_end,
                            latlon=True, meta=True)
        w_cross = vertcross(w, ht, wrfin=wrf_file,
                            start_point=cross_start,
                            end_point=cross_end,
                            latlon=True, meta=True)
        # Para agregar los atributos a la variable (opcional) 
        var_cross.attrs.update(var_cross.attrs)
        w_cross.attrs.update(w_cross.attrs)
        
        # Se hace un interpolado entre los valores 
        # proximos a la topografia y los NaN para que
        # quede mas lindo el grafico.
        var_cross_filled = np.ma.copy(to_np(var_cross))
        w_cross_filled = np.ma.copy(to_np(w_cross))
        
        for i in range(var_cross_filled.shape[-1]):
                column_vals = var_cross_filled[:,i]
                first_idx = int(np.transpose((column_vals > -200).nonzero())[0])
                var_cross_filled[0:first_idx, i] = var_cross_filled[first_idx, i]
        for i in range(w_cross_filled.shape[-1]):
                column_vals = w_cross_filled[:,i]
                first_idx = int(np.transpose((column_vals > -200).nonzero())[0])
                w_cross_filled[0:first_idx, i] = w_cross_filled[first_idx, i]

        # Para sacar las alturas del terreno del corte
        ter_line = interpline(ter, wrfin=wrf_file, start_point=cross_start,
                              end_point=cross_end)

        # Sacar las lat/lon
        lats, lons = latlon_coords(var)

        # Sacar la projeccion de cartopy
        cart_proj = get_cartopy(var)

        ############# GRAFICADO ############# 
        # Figura
        fig = plt.figure(figsize=(8,6))
        ax_cross = plt.axes()

        ## si se quiere tener un intervalo para los datos 
        #var_levels = np.arange(5, 100., 10.)

        # Se hace el grafico de la variable 
        xs = np.arange(0, var_cross.shape[-1], 1)
        ys = to_np(var_cross.coords["vertical"])
        tita_contours = ax_cross.contour(xs,
                                         ys,
                                         to_np(var_cross_filled),
                                         35,
                                         colors='black')
        plt.clabel(tita_contours, inline=1, fontsize=10, fmt="%i")
        # Se hacen los sombreados de la velocidad vertical
        w_sombreado = ax_cross.contourf(xs,
                                        ys,
                                        to_np(w_cross_filled),
                                        np.arange(-1,1,0.1),
                                        cmap = cmap,
                                        extend = 'both')
        cb_w = fig.colorbar(w_sombreado, ax=ax_cross)
        cb_w.ax.tick_params(labelsize=8)

        # Se enmascara la montania con color marron (se cambia en facecolor) 
        ht_fill = ax_cross.fill_between(xs, 0, to_np(ter_line),
                                        facecolor="black")

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

        # para escribir el titulo
        if tidx == 0 :
                dd = 0
                ax_cross.set_title("Corte vertical de tita (k) y vvel (m s-1) en " + str((t_ini)))
                plt.show()
                continue
        if tidx > 0 :
                dd = dd + 3 
                ax_cross.set_title("Corte vertical de tita (k) y vvel (m s-1) en " + str((t_ini+timedelta(hours=dd))))
                plt.show()

