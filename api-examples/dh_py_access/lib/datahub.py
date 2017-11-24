# -*- coding: utf-8 -*-

# from lib.datasets import datasets
from . datasets import datasets

class datahub:
    def __init__(self,server,version,apikey):
        self.server=server
        self.version=version
        self.apikey=apikey

    def init_datasets(self):
        self.datasets=datasets(self.apikey,server=self.server,version=self.version)
        self.dataset_list=self.datasets.dataset_list.r.json()
    

class datahub_main(datahub):
    def __init__(self,apikey):
        self.server="api.planetos.com"
        self.version="v1"
        self.apikey=apikey
        self.init_datasets()
    
        
