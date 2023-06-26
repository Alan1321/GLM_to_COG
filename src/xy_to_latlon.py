import numpy as np
import math

def xy_to_latlon_main(xx, yy, file):
    return xy_to_latlon_1(xx, yy)

def xy_to_latlon_1(xx, yy, file):
    #perform operation
    lat, lon = np.zeros(len(xx)), np.zeros(len(yy))
    return lat, lon

def xy_to_latlon_ghrc_code(xx, yy, file):
    r_eq = file['goes_imager_projection'].semi_major_axis
    #radius of Earth at the pole in meters
    r_pol = file['goes_imager_projection'].semi_minor_axis
    #distance from satellite to earth center in meters
    H = file['goes_imager_projection'].perspective_point_height+r_eq
    #longitude of projection origin in units of radians
    lon0 = file['goes_imager_projection'].longitude_of_projection_origin * (math.pi/180.)
    
    