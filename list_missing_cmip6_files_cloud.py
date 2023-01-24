#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
List missing instance_id's on Google cloud compared to ESGF

@author: timhermans
"""

from pangeo_forge_esgf.parsing import parse_instance_ids
from collections import defaultdict
import pandas as pd
import intake

df = pd.read_csv('https://storage.googleapis.com/cmip6/cmip6-zarr-consolidated-stores.csv')
df.head()
col = intake.open_esm_datastore("https://storage.googleapis.com/cmip6/pangeo-cmip6.json")


experiment_id = ['ssp126','ssp245','ssp370','ssp585','historical']
variable_id = ['psl','pr','sfcWind']

esgf_list = defaultdict(dict)
missing_on_cloud = defaultdict(dict)

for experiment in experiment_id:
    for variable in variable_id:
        if experiment =='historical': #generate idss
            parse_iids = [
                "CMIP6.CMIP.*.*."+experiment+".*.day."+variable+".*.*"
                
            ]
        else:
            parse_iids = [
                "CMIP6.ScenarioMIP.*.*."+experiment+".*.day."+variable+".*.*"
                
            ]
        iids = []
        for piid in parse_iids:
            iids.extend(parse_instance_ids(piid))
        iids.sort()
        esgf_list[experiment][variable] = iids #store ESGF ids
        
        
        query = dict( #start query google cloud
            experiment_id=experiment, 
            table_id='day',                            
            variable_id=variable
        )
        
        col_subset = col.search(**query)
        
        col_subset.df['version']= 'v'+col_subset.df['version'].astype(str) #generate compatible instance_ids
        col_subset.df['instance_id'] = 'CMIP6.'+col_subset.df['activity_id'].str.cat(col_subset.df[['institution_id','source_id','experiment_id','member_id','table_id','variable_id','grid_label','version']], sep='.')

        missing_on_cloud[experiment][variable] = [instance for instance in esgf_list[experiment][variable] if instance not in list(col_subset.df['instance_id'].values)] #compare and store missing ids