import xarray as xr
import numpy as np
import rioxarray as rxr
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling
import cartopy.crs as ccrs

def load_file(infile_location):
    file = xr.open_dataset(infile_location, engine="netcdf4", decode_coords='all', decode_times=False)
    print(file.rio)
    return file

def cartopy_main(infile_location):
    file = load_file(infile_location)
    geostationary_crs = ccrs.Geostationary(
        central_longitude=-75.0,
        satellite_height=35786023.0,
        false_easting=0,
        false_northing=0,
        globe=None,
    )
    ##print(geostationary_crs.__dict__)
    dst_crs = geostationary_crs.proj4_init
    dst_transform, dst_width, dst_height = calculate_default_transform({'init': 'EPSG:4326'}, dst_crs,5424,5424,-135.2,-57.0,-14.2,57.0)
    dst_meta = {
        'driver': 'GTiff',
        'dtype': type(file['Flash_extent_density'].data),
        'nodata': np.nan,
        'width': dst_width,
        'height': dst_height,
        'count': 1,
        'crs': dst_crs,
        'transform': dst_transform,
        'shape':1
    }
    shape=0
    output_path = 'path_to_save_cog_image.tif'
    with rasterio.open(file['Flash_extent_density'].data, output_path, 'w', **dst_meta) as dst:
        reproject(
            source=file['Flash_extent_density'].data,
            destination=rasterio.band(dst, 1),
            src_transform=file.x,
            src_crs='epsg:4326',
            dst_transform=dst_transform,
            dst_crs=dst_crs,
            resampling=Resampling.nearest
        )