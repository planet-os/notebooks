
import numpy as np
from dh_py_access import package_api
import dh_py_access.lib.datahub as datahub
import warnings
warnings.filterwarnings('ignore')

server = 'api.planetos.com'
API_key = open('APIKEY').readlines()[0].strip() #'<YOUR API KEY HERE>'
version = 'v1'

dh=datahub.datahub(server,version,API_key)
dataset='bom_clim_australia'
variable_names = 'tmax'
time_start = '2018-03-01T00:00:00'
time_end = '2019-12-31T23:00:00'
area_name = 'Australia'
latitude_north = -10; latitude_south = -44.5
longitude_west = 112; longitude_east = 157

package = package_api.package_api(dh,dataset,variable_names,longitude_west,longitude_east,latitude_north,latitude_south,time_start,time_end,area_name=area_name +  '_' +variable_names)
package.make_package()
package.download_package()
