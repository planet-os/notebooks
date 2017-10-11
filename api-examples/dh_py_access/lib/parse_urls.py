# -*- coding: utf-8 -*-


import requests


class parse_urls:
    def __init__(self,host,version,endpoint,apikey,**kwargs):
        """
        host: like api.planetos.com/
        """
        reqstr="https://{0}/{1}/{2}?apikey={3}".format(host,version,endpoint,apikey)
        for i,j in kwargs.items():
            reqstr += "&{0}={1}".format(i,j)
        self.r = requests.get(reqstr)
        
