import os
import xarray as xr
import fnmatch

def preprocess(ds):
    ds = ds.expand_dims(dim={"source_id": [ds.source_id]})
    return ds

def open_CMIP6_num_joint_extremes(in_dir,ssps):
    #opens all datasets containing joint extreme statistics for each CMIP6 model in in_dir

    ds_fns = [] #get filenames in input directory
    for top, dirs, files in os.walk(in_dir):
        for file in files:
            ds_fns.append(os.path.join(top, file))

    ssps_ds = [] #load datasets for each ssp
    for ssp in ssps:
        ssp_fns = fnmatch.filter(ds_fns,'*'+ssp+'*')
        ssp_ds = xr.open_mfdataset((ssp_fns),preprocess=preprocess,coords='minimal').chunk({'member_id':200})
        ssps_ds.append(ssp_ds)

    numex_ds = xr.concat(ssps_ds,dim='ssp') #concatenate datasets for each ssps
    numex_ds = numex_ds.assign_coords({'ssp':ssps})
    
    return numex_ds


def open_CMIP6_num_joint_extremes_wp(sfcWind_pr_dir,surge_pr_dir,ssps):
    #opens all datasets containing joint extreme statistics for sfcWind and pr for each CMIP6 model in sfcWind_pr_dir if that dataset also exists in surge_pr_dir

    ds_fns = [] #get filenames wind & pr
    for top, dirs, files in os.walk(sfcWind_pr_dir):
        for file in files:
               ds_fns.append(os.path.join(top, file))

    ds_surge_fns = [] #get filenames surge & pr
    for top, dirs, files in os.walk(surge_pr_dir):
        for file in files:
               ds_surge_fns.append(os.path.join(top, file))          

    #we have more availability for sfcWind than surge (also needs psl), only open the overlapping files here
    ssps_ds = []
    for ssp in ssps:
        ssp_fns = fnmatch.filter(ds_fns,'*'+ssp+'*')
        ssp_surge_fns = fnmatch.filter(ds_surge_fns,'*'+ssp+'*')
        ssp_fns = [f for f in ssp_fns if '/'.join(f.split('/')[-2::]) in ['/'.join(k.split('/')[-2::]) for k in ssp_surge_fns]]
        ssp_ds = xr.open_mfdataset((ssp_fns),preprocess=preprocess,coords='minimal').chunk({'member_id':200})
        ssps_ds.append(ssp_ds)

    numex_ds = xr.concat(ssps_ds,dim='ssp')
    numex_ds = numex_ds.assign_coords({'ssp':ssps})

    return numex_ds


