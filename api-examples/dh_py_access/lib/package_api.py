import requests
import os
import sys
import time
import json
import zipfile

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


def unzip(package_key):
    folder = os.path.dirname(os.path.realpath(__file__)) + '/'
    zip_filename = package_key + '.zip'
    zip_ref = zipfile.ZipFile(zip_filename, 'r')
    zip_ref.extract('data',)
    zip_ref.close()
    os.remove(zip_filename)
    os.rename(folder + 'data', folder + package_key + '.nc')