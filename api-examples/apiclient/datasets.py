# -*- coding: utf-8 -*-

# from lib.parse_urls import parse_urls
from . parse_urls import parse_urls

class datasets:
    def __init__(self,apikey,server="api.planetos.com",version="v1",endpoint="datasets", debug=False):
        self.dataset_list=parse_urls(server,version,endpoint,apikey, debug=debug)


if __name__=="__main__":
    abc=datasets()
    print(abc.dataset_list.r.json())

