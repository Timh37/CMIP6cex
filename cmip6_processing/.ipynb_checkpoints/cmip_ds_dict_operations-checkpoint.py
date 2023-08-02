import xarray as xr
import numpy as np
from collections import defaultdict

def preselect_years(ddict_in,start_year,end_year):
    '''trim time periods of datasets in dictionary of datasets, historical and ssp runs must be separate'''
    ddict_out = defaultdict(dict)
    
    assert start_year<end_year
        
    if start_year>2014: #only using SSP
        for k, v in ddict_in.items():
            if 'ssp' in k:
                ddict_out[k] = v.sel(time=slice(str(start_year), str(end_year)))
                
    elif end_year<=2014: #only using historical
        for k, v in ddict_in.items():
            if 'historical' in k:
                ddict_out[k] = v.sel(time=slice(str(start_year), str(end_year)))
                
    elif ((start_year<=2014) & (end_year>2014)): #using both
        for k, v in ddict_in.items():
            if 'ssp' in k:
                ddict_out[k] = v.sel(time=slice('2015', str(end_year)))
            elif 'historical' in k:
                ddict_out[k] = v.sel(time=slice(str(start_year), '2014'))
    return ddict_out #NB: may result in no timesteps being selected at all

def pr_flux_to_m(ddict_in):
    '''convert pr flux to total accumulated pr'''
    ddict_out = ddict_in
    for k, v in ddict_in.items():
        assert v.pr.units == 'kg m-2 s-1'
        
        with xr.set_options(keep_attrs=True): #convert 'kg m-2 s-1' to daily accumulated 'm'
            v['pr'] = 24*3600*v['pr']/1000 #multiply by number of seconds in a day to get to kg m-2, and divide by density (kg/m3) to get to m    
        v.pr.attrs['units'] = 'm'
        
        ddict_out[k] = v
    return ddict_out

def drop_duplicate_timesteps(ddict_in):
    '''removes duplicate timesteps present in some CMIP6 models'''
    ddict_out = ddict_in
    for k, v in ddict_in.items():  
        unique_time, idx = np.unique(v.time,return_index=True)
        
        if len(v.time) != len(unique_time):
            ddict_out[k] = v.isel(time=idx)
            print('Dropping duplicate timesteps for:' + k)   
    return ddict_out

def drop_coords(ddict_in,coords_to_drop):
    '''remove some coordinates present we don't need'''
    for k, v in ddict_in.items():
        ddict_in[k] = v.drop_dims(coords_to_drop,errors="ignore")
    return ddict_in