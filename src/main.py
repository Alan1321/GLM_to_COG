from lmatools.grid.fixed import get_GOESR_coordsys
import math
import xarray as xr
import numpy as np

file_location1 = "/home/asubedi/Desktop/data/raw-files/GLM/OR_GLM-L3-GLMF-M6_G16_s202315823490000_e202315823500000_c20231582351080.nc"
variable1 = "Flash_extent_density"
file1 = xr.open_dataset(file_location1, engine="netcdf4", decode_coords='all', decode_times=False)
#radius of Earth at the equator in meters
r_eq = file1['goes_imager_projection'].semi_major_axis

#radius of Earth at the pole in meters
r_pol = file1['goes_imager_projection'].semi_minor_axis

#distance from satellite to earth center in meters
H = file1['goes_imager_projection'].perspective_point_height+r_eq

#longitude of projection origin in units of radians
lon0 = file1['goes_imager_projection'].longitude_of_projection_origin * (math.pi/180.)

x_1d = file1.x
y_1d = file1.y

x,y = np.meshgrid(x_1d, y_1d) # Two 2D arrays of fixed grid coordinates
nadir = -75.0
geofixCS, grs80lla = get_GOESR_coordsys(nadir)
z=np.zeros_like(x)
lon,lat,alt=grs80lla.fromECEF(*geofixCS.toECEF(x,y,z))
lon.shape = x.shape
lat.shape = y.shape

#lat only
# for arry in lat:
#     count = 0
#     total = 0
#     for value in arry:
#         if math.isinf(value) == False:
#             count += 1
#             total += value
#     if count != 0:
#         print(float(total/count), end=" ")
#     else:
#         print("-999.0")

#lon
for i in range(len(lon)):
    count = 0
    total = 0
    for j in range(len(lon)):
        if math.isinf(lon[j][i]) == False:
            count += 1
            total += lon[j][i]
    if count != 0:
        print(float(total/count), end=" ")
    else:
        print("-999.0")