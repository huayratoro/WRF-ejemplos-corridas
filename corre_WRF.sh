#usr/bin/bash
##################### script para correr el WRF desde el namelist.wps #####################
##################### POWERED BY HUAYRATORO #####################
##### IMPORTANTE : Recordar setear bien los namelist WPS, input y ARWpost porque sino tira error... 
## 	Primera parte: WPS
# moverse hacia la carpeta WPS donde estan los tres ejecutables
cd /home/marcos/Build_WRF/WPS/
# Ejecuto el geogrid.exe
./geogrid.exe
###### RECORDAR CREAR EL VTABLE PARA EL GFS O ECMWF EN EL DIRECTORIO ######
###### Sino crear con el comando : ln -sf ungrib/Variable_Tables/Vtable.GFS Vtable
# Una vez creado el Vtable, entonces linkear los grib files, que pueden estar en una caprtea aparte del WPS 
./link_grib.csh /home/marcos/Build_WRF/caso_ejemplo/analysis/gfsanl*
# ahora ejecutar el ungrib.exe
./ungrib.exe
# finalmente ejecutar el metgrid.exe 
./metgrib.exe
##	Segunda parte: WRF
# moverse a la carpeta .../test/em_real de WRF
cd /home/marcos/Build_WRF/WRF/test/em_real/
# linkear la salida de los metgrib a la carpeta WRF
ln -sf /home/marcos/Build_WRF/WPS/met_em.d01* .
###### RECORDAR EDITAR EL NAMELIST.INPUT DE ACUERDO AL WPS PARA QUE NO TIRE ERROR
# se corre el real.exe
./real.exe
# se corre el wrf.exe
./wrf.exe
##	Tercera parte: ARWpost
# editar el namelist del ARWpost con las fechas y niveles que se quiera 
# moverse a la carpeta del ARWpost
cd /home/marcos/Build_WRF/ARWpost/
# se corre el arw.exe
./ARWpost.exe
###### listo ######
echo 'LISTA LA CORRIDA XD' 
