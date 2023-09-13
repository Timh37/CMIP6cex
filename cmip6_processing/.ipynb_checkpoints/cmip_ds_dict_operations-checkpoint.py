import xarray as xr
import numpy as np
from collections import defaultdict

def select_period(ddict_in,start_year,end_year):
    ddict_out = defaultdict(dict) #initialize output
    
    assert start_year<end_year
        
    for k, v in ddict_in.items():
        ddict_out[k] = v.sel(time=slice(str(start_year), str(end_year)))
       
    return ddict_out

def pr_flux_to_m(ddict_in):
    '''convert pr flux to total accumulated pr'''
    ddict_out = ddict_in
    for k, v in ddict_in.items():
        if 'pr' in v.variables:
            assert v.pr.units == 'kg m-2 s-1'

            with xr.set_options(keep_attrs=True): #convert 'kg m-2 s-1' to daily accumulated 'm'
                v['pr'] = 24*3600*v['pr']/1000 #multiply by number of seconds in a day to get to kg m-2, and divide by density (kg/m3) to get to m    
            v.pr.attrs['units'] = 'm'
        
        ddict_out[k] = v
    return ddict_out

def drop_duplicate_timesteps(ddict_in):
    '''removes duplicate timesteps in CMIP6 simulations in dictionary if present'''
    ddict_out = ddict_in
    for k, v in ddict_in.items():  
        unique_time, idx = np.unique(v.time,return_index=True)
        
        if len(v.time) != len(unique_time):
            ddict_out[k] = v.isel(time=idx)
            print('Dropping duplicate timesteps for:' + k)   
    return ddict_out

def drop_coords(ddict_in,coords_to_drop):
    '''remove coordinates from datasets in dictionary'''
    for k, v in ddict_in.items():
        ddict_in[k] = v.drop_dims(coords_to_drop,errors="ignore")
    return ddict_in

def drop_incomplete(ddict_in):
    ddict_out = defaultdict(dict)
    
    for k, ds in ddict_in.items():
        
        time_diff = ds.time.diff('time').astype(int)
        mean_time_diff = time_diff.mean()
        normalized_time_diff = abs((time_diff - mean_time_diff)/mean_time_diff)
        
        # do not include datasets with time not increasing monotonically
        if (time_diff > 0).all() == False: 
            continue
        
        # do not include datasets with large time gaps
        if (normalized_time_diff>0.05).all():
            continue
        
        ddict_out[k] = ds
    return ddict_out