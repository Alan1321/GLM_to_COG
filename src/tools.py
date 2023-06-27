# from lmatools.grid.fixed import get_GOESR_coordsys
import math
import xarray as xr
import numpy as np
import random

def load_file(infile_location):
    file = xr.open_dataset(infile_location, engine="netcdf4", decode_coords='all', decode_times=False)
    print(file.rio)
    return file

def trim_data(lat, lon, data):
    """
    Removing rows and columns of data with lat, lon value of -999

    Args:
        lat, lon (List): 1D Numpy array with lat, lon, data
    
    Returns:
        List: list of trimmed data
    """
    _lat = lat.copy()
    _lon = lon.copy()
    _data = data.copy()

    end_index = len(lon)
    for index, value in np.ndenumerate(lon[::-1]):
        end_index -= 1
        if value == -999.0:
            _data = np.delete(_data, end_index, axis=0)
            _lon = np.delete(_lon, end_index)

    end_index = len(lat)
    for index, value in np.ndenumerate(lat[::-1]):
        end_index -= 1
        if value == -999.0:
            _data = np.delete(_data, end_index, axis=1)
            _lat = np.delete(_lat, end_index)
    
    return _lat, _lon, _data

def new_xrDataset(lat, lon, data, data_var, instrument_name):
    """
    Generating a new netcdf file

    Args:
        lat (List): Numpy array of latitude data
        lon (List): Numpy array of longitude data
        data (List): 2D Numpy array of data values
    """
    file = xr.Dataset(
        data_vars={data_var: (("lon", "lat"), data)},
        coords={"lon": lon, "lat": lat},
        attrs={"instrument_name": instrument_name}
    )
    print(file.rio)
    return file

def to_netcdf(file, variable_name, outfile_location, total):
    """
    Converting a given xarray Dataset file to nc
    """
    file = file[variable_name]
    file = conversion(file)
    outfile_name = f"new_netcdf4_{random_number_generator(total)}.nc"
    outfile_location = outfile_location + '/' + outfile_name
    file.to_netcdf(outfile_location)
    print(f"--> New netcdf4 file {outfile_name} has been generated. Path: {outfile_location}")

def to_geotiff(file, variable_name, outfile_location, total):
    """
    Converting a netcdf file to geotiff image

    Args:
        infile_location (string): Location of the netcdf file
        variable_name (string): Variable name in the file to be converted
    """
    file = file[variable_name]

    file = file.transpose("lat", "lon") 
    file.rio.set_spatial_dims(x_dim='lon', y_dim='lat', inplace=True)
    file.rio.crs
    file.rio.set_crs('epsg:4326', inplace=True)

    outfile_name = f"S2A_20160724_135032_27XVB_B{random_number_generator(total)}.tif"
    outfile_location = outfile_location + '/' + outfile_name
    file.rio.to_raster(rf'{outfile_location}', driver="COG")
    print(f"--> New geotiff file {outfile_name} has been generated. Path: {outfile_location}")

def conversion(file, transpose=True):
    """
    """
    file = file.transpose("lat", "lon") if transpose == True else file
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
    for t in range(total):
        digit += str(random.randint(0,9))
    return digit