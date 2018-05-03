# -*- coding: utf-8 -*-


import requests


class parse_urls:
    def __init__(self,host,version,endpoint,apikey,debug=False,**kwargs):
        """
        host: like api.planetos.com/
        """
        reqstr="http://{0}/{1}/{2}?apikey={3}".format(host, version, endpoint, apikey)
        for i,j in kwargs.items():
            reqstr += "&{0}={1}".format(i,j)
        if debug:
            print('reqstr',reqstr)
        self.r = requests.get(reqstr)
        
