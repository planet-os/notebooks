import requests
import os
import sys
import time
import json
import zipfile

def generate_links(folder,dataset_key,API_key,longitude_west,longitude_east,latitude_south,latitude_north,time_start,time_end,variable,area):
    package_key_nr = time_start + 'to' + time_end; package_key_nr = package_key_nr.replace('-','').replace(':','')
    package_key = dataset_key + '_' + package_key_nr + '_' + area
    put_http = 'https://api.planetos.com/v1/packages?dataset={0}&apikey={1}&polygon=[[{2},{4}],[{3},{4}],[{3},{5}],[{2},{5}],[{2},{4}]]&grouping=location&reftime_recent=true&time_start={6}&time_end={7}&package={8}&var={9}&count=1000'.format(dataset_key,API_key,longitude_west,longitude_east,latitude_south,latitude_north,time_start,time_end,package_key,variable)
    get_status_http = 'https://api.planetos.com/v1/packages/{0}?apikey={1}'.format(package_key,API_key)
    get_data_http = 'https://api.planetos.com/v1/packages/{0}/data?apikey={1}'.format(package_key,API_key)
    #print (put_http)
    print (get_status_http)
    #print (get_data_http)
    return package_key, put_http, get_status_http, get_data_http

def generate_links_station(folder,dataset_key,API_key,station_id,time_start,time_end,variable,area):
    package_key_nr = time_start + 'to' + time_end; package_key_nr = package_key_nr.replace('-','').replace(':','')
    package_key = dataset_key + '_' + package_key_nr + '_' + area
    put_http = 'https://api.planetos.com/v1/packages?dataset={0}&apikey={1}&station={2}&grouping=location&reftime_recent=true&time_start={3}&time_end={4}&package={5}&var={6}'.format(dataset_key,API_key,station_id,time_start,time_end,package_key,variable)
    get_status_http = 'https://api.planetos.com/v1/packages/{0}?apikey={1}'.format(package_key,API_key)
    get_data_http = 'https://api.planetos.com/v1/packages/{0}/data?apikey={1}'.format(package_key,API_key)
    print (put_http)
    print (get_status_http)
    print (get_data_http)
    return package_key, put_http, get_status_http, get_data_http

def make_package(put_http,get_status_http):
    r_get = requests.get(get_status_http)
    r_get_content = r_get.content.decode("utf-8")
    if r_get_content == 'Package not found':
       r = requests.put(put_http)
       put_status = r.status_code
       print ('Please wait while package is downloaded')
       time.sleep(10)
    else:
        stats_json = json.loads(r_get_content)
        if 'packageResult' in stats_json:
            if stats_json['packageResult']['success'] == True:
                put_status = 200
        else:
            r = requests.put(put_http)
            put_status = r.status_code
            print ('Please wait while package is downloaded')
            time.sleep(10)
    if not put_status == 200:
        print ('Package creation was unsuccessful with status: ' + put_status)
        print ('Please try again!')
        sys.exit()




def get_package(get_data_http,get_status_http,package_key):
    r_get = requests.get(get_status_http)
    r_get_content = r_get.content.decode("utf-8")
    stats_json = json.loads(r_get_content)
    if 'packageResult' in stats_json:
        if stats_json['packageResult']['success'] == True:
            if 'does not contain' in stats_json['packageStatus']['message']:
                raise Exception((str(stats_json['packageStatus']['message'])) + ' Please choose another date')
                
            else:
                r = requests.get(get_data_http,stream = True)
                if r.status_code == 200:
                     with open(package_key + ".zip", "wb") as dat:
                        dat.write(r.content)
                else:
                    print ('something happened while downloading data. Please try again.')
                    sys.exit()
                status = 'Package downloaded'
        else:
        	status = 'Package not downloaded'
    else:
        status = 'Package not downloaded'
    return status


def unzip(package_key,folder):
    zip_filename = package_key + '.zip'
    zip_ref = zipfile.ZipFile(zip_filename, 'r')
    zip_ref.extractall(folder,)
    zip_ref.close()
    os.remove(zip_filename)
    if not os.path.exists(folder + '/data'):
        files = os.listdir(folder + '/nodestation/')
        os.rename(folder + '/nodestation/' + files[0] + '/data',folder + package_key + '.nc')
    else:
        os.rename(folder + 'data', folder + package_key + '.nc')

def download_data(folder,dataset_key,API_key,longitude_west,longitude_east,latitude_south,latitude_north,time_start,time_end,variable,area):
    package_key, put_http, get_status_http, get_data_http = generate_links(folder,dataset_key,API_key,longitude_west,longitude_east,latitude_south,latitude_north,time_start,time_end,variable,area)
    if not os.path.exists(folder + '/' + package_key + '.nc'):
        make_package(put_http,get_status_http)
        get_stats = get_package(get_data_http,get_status_http,package_key)
        if get_stats == 'Package not downloaded':
            print ('Package download was unsuccessful, please wait a few seconds...')
            time.sleep(10)
            get_stats2 = get_package(get_data_http,get_status_http,package_key)
        elif get_stats == 'Package downloaded':
            print ('Data is downloaded!')
            unzip(package_key,folder)
    else:
        print ('file already exists, no need to download other one')
    return package_key

def download_data_station(dataset_key,API_key,station_id,time_start,time_end,variable,area):
    folder = os.path.dirname(os.path.realpath(__file__))
    print (folder)
    package_key, put_http, get_status_http, get_data_http = generate_links_station(folder,dataset_key,API_key,station_id,time_start,time_end,variable,area)
    if not os.path.exists(folder + '/' + package_key + '.nc'):
        make_package(put_http,get_status_http)
        get_stats = get_package(get_data_http,get_status_http,package_key)
        if get_stats == 'Package not downloaded':
            print ('Package download was unsuccessful, please wait a few seconds...')
            time.sleep(15)
            get_stats2 = get_package(get_data_http,get_status_http,package_key)
        elif get_stats == 'Package downloaded':
            print ('Data is downloaded!')
            unzip(package_key,folder)
    else:
        print ('file already exists, no need to download other one')
    return package_key
