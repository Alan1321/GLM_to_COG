from lmatools.grid.fixed import get_GOESR_coordsys
import math
import xarray as xr
import numpy as np
import random

def load_file(infile_location):
    return xr.open_dataset(infile_location, engine="netcdf4", decode_coords='all', decode_times=False)

def get_variable_information(file):
    r_eq = file['goes_imager_projection'].semi_major_axis
    #radius of Earth at the pole in meters
    r_pol = file['goes_imager_projection'].semi_minor_axis
    #distance from satellite to earth center in meters
    H = file['goes_imager_projection'].perspective_point_height+r_eq
    #longitude of projection origin in units of radians
    lon0 = file['goes_imager_projection'].longitude_of_projection_origin * (math.pi/180.)
    return r_eq, r_pol, H, lon0

def xy_to_latlon(xx, yy):
    lat, lon = 0,0
    return lat, lon

def new_xrDataset(lat, lon, data):
    """
    Generating a new netcdf file

    Args:
        lat (List): Numpy array of latitude data
        lon (List): Numpy array of longitude data
        data (List): 2D Numpy array of data values
    """
    file = xr.Dataset(
        data_vars={"Flash_extent_density": (("lon", "lat"), data)},
        coords={"lon": lon, "lat": lat},
        attrs={"instrument_ID": "GLM-1"}
    )
    return file

def to_netcdf(file, variable_name):
    """
    Converting a given xarray Dataset file to nc
    """
    file = file[variable_name]
    file = conversion(file)



def to_geotiff(infile_location, variable_name):
    """
    Converting a netcdf file to geotiff image

    Args:
        infile_location (string): Location of the netcdf file
        variable_name (string): Variable name in the file to be converted
    """
    file = load_file(infile_location)

def conversion(file):
    """
    """
    file = file.transpose("lat", "lon")
    file.rio.set_spatial_dims(x_dim='lon', y_dim='lat', inplace=True)
    file.rio.crs
    file.rio.set_crs('epsg:4326', inplace=True)
    return file

def random_number_generator(total):
    """
    Generating a random number

    Args:
        total (int): How many digits to generate
    
    Returns
        string: Random number
    """
    digit = ""
    for t in total:
        digit += str(random.randint(0,9))
    return digit