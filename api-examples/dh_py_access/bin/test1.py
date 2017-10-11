# -*- coding: utf-8 -*-

from lib.datahub import datahub_main as dhm
from lib.dataset import dataset

## define datahub parameters
abc=dhm("804e22da0c704d7b955a3d250750bc2b")

## list datasets to find useful etc,
## print(abc.dataset_list)
## define dataset
gfs=dataset('noaa_gfs_pgrb2_global_forecast_recompute_0.25degree',abc)
## list or filter variables by long_name, standard_name, etc
## print([j['attributes'] for i in gfs.variables() for j in i])
print(gfs.standard_names)
