from tools import load_file, trim_data, new_xrDataset, to_geotiff, to_netcdf
from xy_to_latlon import xy_to_latlon_main

#Variables
infile_location = "/home/asubedi/Desktop/data/raw-files/GLM/OR_GLM-L3-GLMF-M6_G16_s202315823490000_e202315823500000_c20231582351080.nc"
outfile_location = "/home/asubedi/Desktop/test/"
total_random_number = 5
variable_name = "Flash_extent_density"

#for new xarray formation
data_variable_name = "Flash Extent Density"
instrument_name = "GLM-3"

def start():
    file = load_file(infile_location)
    lat, lon = xy_to_latlon_main(file.x, file.y, file)
    lat, lon, data = trim_data(lat, lon, file.data)
    file2 = new_xrDataset(lat, lon, data, data_variable_name, instrument_name)
    to_geotiff(file2, variable_name, outfile_location, total_random_number)
    to_netcdf(file2, variable_name, outfile_location, total_random_number)

start()