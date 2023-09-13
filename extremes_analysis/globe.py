import numpy as np
import os

#from https://github.com/toddkarin/global-land-mask

# Load the data from file.
#full_path = os.path.realpath(__file__)
#_path, _ = os.path.split(full_path)


_mask_fid = np.load('globe_combined_mask_compressed.npz')

_mask = _mask_fid['mask']
_lat = _mask_fid['lat']
_lon = _mask_fid['lon']


def lat_to_index(lat):
    """
    Convert latitude to index on the mask

    Parameters
    ----------
    lat : numeric
        Latitude to get in degrees

    Returns
    -------
    index : numeric
        index of the latitude axis.

    """
    lat = np.array(lat)

    if np.any(lat>90):
        raise ValueError('latitude must be <= 90')

    if np.any(lat<-90):
        raise ValueError('latitude must be >= -90')


    lat[lat > _lat.max()] = _lat.max()
    lat[lat < _lat.min()] = _lat.min()

    return ((lat - _lat[0])/(_lat[1]-_lat[0])).astype('int')




def lon_to_index(lon):
    """
    Convert longitude to index on the mask

    Parameters
    ----------
    lon : numeric
        Longitude to get in degrees

    Returns
    -------
    index : numeric
        index of the longitude axis.

    """

    lon = np.array(lon)

    if np.any(lon > 180):
        raise ValueError('longitude must be <= 180')

    if np.any(lon < -180):
        raise ValueError('longitude must be >= -180')


    lon[lon > _lon.max()] = _lon.max()
    lon[lon < _lon.min()] = _lon.min()


    return ((lon - _lon[0]) / (_lon[1] - _lon[0])).astype('int')



def is_ocean(lat,lon):
    """

    Return boolean array of whether the coordinates are in the ocean

    Parameters
    ----------
    lat : ndarray or float

        latitude in degrees

    lon : ndarray or float

        longitude in degrees

    Returns
    -------
    is_ocean_mask : ndarray or float

        boolean array denoting whether the corresponding point is in the ocean.
    """
    lat_i = lat_to_index(lat)
    lon_i = lon_to_index(lon)

    return _mask[lat_i,lon_i]


def is_land(lat,lon):
    """

    Return boolean array of whether the coordinates are on the land. Note
    that most lakes are considered on land.

    Parameters
    ----------
    lat : ndarray or float

        latitude in degrees

    lon : ndarray or float

        longitude in degrees

    Returns
    -------
    is_land_mask : ndarray or float

        boolean array denoting whether the corresponding point is on land.

    """
    lat_i = lat_to_index(lat)
    lon_i = lon_to_index(lon)

    return np.logical_not(_mask[lat_i,lon_i])