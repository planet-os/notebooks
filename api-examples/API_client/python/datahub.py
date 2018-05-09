# -*- coding: utf-8 -*-

import os
from API_client.python.lib.datasets import datasets


class datahub:
    def __init__(self,server,version,apikey=''):
        self.server=server
        self.version=version
        self.apikey=apikey
        self.get_apikey()

    def get_apikey(self):
        if len(self.apikey)==0:
            assert os.path.exists('APIKEY'), "apikey must be given to datahub as argument or saved in the work folder in file APIKEY"
            self.apikey = open('APIKEY').readlines()[0].strip()
        else:
            print("did not update apikey")

    def init_datasets(self):
        self.datasets=datasets(self.apikey,server=self.server,version=self.version)
        self.dataset_list=self.datasets.dataset_list.r.json()
    

class datahub_main(datahub):
    def __init__(self,apikey=''):
        self.server="api.planetos.com"
        self.version="v1"
        self.apikey=apikey
        self.init_datasets()
    
        
