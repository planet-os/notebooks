
from API_client.python.lib.dataset import dataset
import dh_py_access.lib.datahub as datahub
from dh_py_access import package_api
import datetime
server = 'http://api.planetos.com/v1/datasets/'
API_key = open('APIKEY').read().strip()
today = datetime.datetime.today()
two_days_ago = today - datetime.timedelta(days=1)


two_days_ago_str = datetime.datetime.strftime(two_days_ago, '%Y-%m-%dT') + '12:00:00'
dh=datahub.datahub_main(API_key)
ds = dataset('noaa_rbsn_timeseries',dh)

fmi_hirlam_surface=dataset('fmi_hirlam_surface',dh)
metno_harmonie_metcoop=dataset('metno_harmonie_metcoop',dh)
gfs=dataset('noaa_gfs_pgrb2_global_forecast_recompute_0.25degree',dh)
sample_var_names = {fmi_hirlam_surface:'Temperature_height_above_ground',
                    metno_harmonie_metcoop:'air_temperature_2m',
                    gfs:'tmp_m'}
obs_data = ds.get_station_data_as_pandas(['26233'],variables='temperature',start = two_days_ago_str)
longitude= 25.60
latitude = 58.36

sample_point_data = [(k,k.get_json_data_in_pandas(**{'var':v,'lon':longitude,'lat':latitude,'count':1000,'reftime_start':two_days_ago_str,'reftime_end':two_days_ago_str})) for k,v in sample_var_names.items()]