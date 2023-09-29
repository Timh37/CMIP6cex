#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
List instance_id's on ESGF that are not on Google cloud. This can be used to request new iid's from https://github.com/leap-stc/cmip6-leap-feedstock/issues, for instance.

@author: timhermans
"""
from pangeo_forge_esgf.parsing import parse_instance_ids
from collections import defaultdict
import pandas as pd
import intake

df = pd.read_csv('https://storage.googleapis.com/cmip6/cmip6-zarr-consolidated-stores.csv')
df.head()
col = intake.open_esm_datastore("https://storage.googleapis.com/cmip6/pangeo-cmip6.json")

#experiment_id = ['ssp126','ssp245','ssp370','ssp585','historical']
experiment_id = ['ssp585','historical']
variable_id = ['psl','pr','sfcWind']

source_id = ['BCC-CSM2-MR','CESM2','CESM2-WACCM','CMCC-ESM2','CMCC-CM2-SR5','EC-Earth3',
                'GFDL-CM4','GFDL-ESM4','HadGEM3-GC31-MM','MIROC6','MPI-ESM1-2-HR','MRI-ESM2-0',
                'NorESM2-MM','TaiESM1']

esgf_list = []
missing_on_cloud = []

for variable in variable_id:
    for experiment in experiment_id:
        for source in source_id:
            if experiment =='historical': #generate idss
                parse_iids = [
                    "CMIP6.CMIP.*."+source+"."+experiment+".*.day."+variable+".*.*"    
                ]
            else:
                parse_iids = [
                    "CMIP6.ScenarioMIP.*."+source+"."+experiment+".*.day."+variable+".*.*"   
                ]
            iids = []
            for piid in parse_iids:
                iids.extend(parse_instance_ids(piid))
            iids.sort()
            esgf_list.extend(iids)
            
            query = dict( #start query google cloud
                experiment_id=experiment, 
                table_id='day',                            
                variable_id=variable,
                source_id=source
            )
            
            col_subset = col.search(**query)
            
            col_subset.df['version']= 'v'+col_subset.df['version'].astype(str) #generate compatible instance_ids
            col_subset.df['instance_id'] = 'CMIP6.'+col_subset.df['activity_id'].str.cat(col_subset.df[['institution_id','source_id','experiment_id','member_id','table_id','variable_id','grid_label','version']], sep='.')
    
            iids_not_on_cloud = [instance for instance in iids if instance not in list(col_subset.df['instance_id'].values)] #compare and store missing ids
            missing_on_cloud.extend(iids_not_on_cloud)
            
