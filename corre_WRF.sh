#usr/bin/bash
##################### script para correr el WRF con algun caso real #####################
##################### POWERED BY HUAYRATORO #####################
# Este bash solo corre con todas las librerias instaladas y los WPS, WRF y ARWpost compilados
# para mas info sobre como setear el env e instalar librerias consultar alguno de estos enlaces :
# https://www2.mmm.ucar.edu/wrf/OnLineTutorial/Introduction/start.php  >> del UCAR (con casos de estudio!)
# https://www.youtube.com/watch?v=_9lBM4k7HQc >> video muy didactico !!
# cambiar las direcciones y rutas a lo adecuado
##### IMPORTANTE : Recordar setear bien los namelist WPS, input y ARWpost porque sino tira error... 
## 	Primera parte: WPS
# moverse hacia la carpeta WPS donde estan los tres ejecutables
cd .../Build_WRF/WPS/
# Ejecuto el geogrid.exe
./geogrid.exe
###### RECORDAR CREAR EL VTABLE PARA EL GFS O ECMWF EN EL DIRECTORIO ######
###### Sino crear con el comando : ln -sf ungrib/Variable_Tables/Vtable.GFS Vtable
# Una vez creado el Vtable, entonces linkear los grib files, que pueden estar en una caprtea aparte del WPS 
./link_grib.csh .../Build_WRF/caso_ejemplo/analysis/gfsanl*
# ahora ejecutar el ungrib.exe
./ungrib.exe
# finalmente ejecutar el metgrid.exe 
./metgrid.exe
##	Segunda parte: WRF
# moverse a la carpeta .../test/em_real de WRF
cd .../Build_WRF/WRF/test/em_real/
# linkear la salida de los metgrib a la carpeta WRF
ln -sf .../Build_WRF/WPS/met_em.d01* .
###### RECORDAR EDITAR EL NAMELIST.INPUT DE ACUERDO AL WPS PARA QUE NO TIRE ERROR
# se corre el real.exe
./real.exe
# se corre el wrf.exe
./wrf.exe
##	Tercera parte: ARWpost
# editar el namelist del ARWpost con las fechas y niveles que se quiera 
# moverse a la carpeta del ARWpost
cd .../Build_WRF/ARWpost/
# se corre el arw.exe
./ARWpost.exe
###### listo ######
echo 'LISTA LA CORRIDA XD' 
