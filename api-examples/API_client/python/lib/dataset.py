# -*- coding: utf-8 -*-

import requests
import pandas as pd
from netCDF4 import Dataset
import datetime
from dateutil.parser import parse
# from lib.parse_urls import parse_urls
from . parse_urls import parse_urls
import collections
import itertools


class dataset:
    def __init__(self,datasetkey,datahub,debug=False):
        self.datasetkey = datasetkey
        self.datahub=datahub
        self.datahub.init_datasets()
        assert datasetkey in self.datahub.dataset_list
        try:
            self.get_reftimes()
            self.get_timesteps()
        except:
            pass
        self.debug = debug

    def variables(self):
        variables=parse_urls(self.datahub.server, self.datahub.version, "datasets/"+self.datasetkey+"/variables", self.datahub.apikey)
        
        return variables.r.json()['variables']

    def variable_names(self):
        return sorted(list(set(list(map(lambda x: x['variableKey'], self.variables())))))

    def standard_names(self):
        """
        return list of standard names of variables
        """
        return self.return_names('standard_name')

    def return_names(self,nameversion):
        """
        return list of variables by name type
        """
        stdnames=[]
        for k in self.variables():
            for j in k:
                if j == 'attributes':
                    for i in k[j]:
                        if i['attributeKey']==nameversion:
                            stdnames.append(i['attributeValue'])
        return sorted(list(set(stdnames)))

    def get_standard_name_from_variable_name(self,varname):
        for i in self.variables():
            if i['variableKey'] == varname:
                for j in i['attributes']:
                    if j['attributeKey']=='long_name':
                        return j['attributeValue']
        
    def long_names(self):
        """
        return list of long names of variables
        """
        return self.return_names('long_name')

    def get_tds_file(self,variable):
        """
        Until something better found ...
        return first file tds path that contains variable name, should work with either standard or long name!
        """

        tdaddr="http://{0}/{1}/data/dataset_physical_contents/{2}?apikey={3}".format(self.datahub.server,self.datahub.version,self.datasetkey,self.datahub.apikey)
        r=requests.get(tdaddr).json()
        for htt in r:
            found_vars=[j for j in htt['variables'] for i in j if j[i]==variable]
            if len(found_vars)>0:
                return htt['planetosOpenDAPVariables']

    def get_tds_field(self,variable):
        stdname=self.get_standard_name_from_variable_name(variable)
        if not stdname:
            stdname=variable
        if len(stdname)==0:
            stdname=variable  
##        print("stdname in get_field",stdname)
        tdsfile=self.get_tds_file(variable)
        assert len(tdsfile)>10, "could not determine TDS path, cannot continue"
##        print('TDS file',tdsfile)
        ds = Dataset(tdsfile)
        vari = ds.variables[variable]
        dimlen = len(vari.dimensions)
        if dimlen==4:
            return vari[0,0,:,:]
        elif dimlen==3:
            return vari[0,:,:]
        elif dimlen==2:
            return vari[:,:]
        else:
            return vari[:]
            ## raise ValueError("Cannot return 2D array for {0}".format(variable))

    def get_json_data_in_pandas(self,count=10,z='all',pandas=True,debug=False,**kwargs):
        def convert_json_to_some_pandas(injson):
            param_list = ['axes','data']
            new_dict = {}
            [new_dict.update({i:[]}) for i in param_list]
            [(new_dict['axes'].append(i['axes']),new_dict['data'].append(i['data'])) for i in injson];
            pd_temp = pd.DataFrame(injson)
            dev_frame = pd_temp[['context','axes']].join(pd.concat([pd.DataFrame(new_dict[i]) for i in param_list],axis=1))
            if 'reftime' in dev_frame.columns:
                ## dev_frame = dev_frame[dev_frame['reftime'] == dev_frame['reftime'][0]]
                for ttt in 'reftime','time':
                    dev_frame[ttt] = dev_frame[ttt].apply(pd.to_datetime)
            else:
                dev_frame['time'] = dev_frame['time'].apply(pd.to_datetime)
            return dev_frame
        if not 'count' in kwargs:
            kwargs['count'] = count
        if not 'z' in kwargs:
            kwargs["z"]=z
        retjson=parse_urls(self.datahub.server, self.datahub.version, "datasets/{0}/point".format(self.datasetkey), self.datahub.apikey, clean_reftime=False, debug=self.debug, **kwargs).r.json()
        if pandas: retjson=convert_json_to_some_pandas(retjson['entries'])
        return retjson

    def stations(self):
        stations = parse_urls(self.datahub.server, self.datahub.version, "datasets/"+self.datasetkey+"/stations", self.datahub.apikey).r.json()
        return stations

    def get_station_data(self, stations=stations, **kwargs):
        requrl = 'datasets/' + self.datasetkey + '/stations/' + stations 
                            
        # for i in kwargs:
        #    requrl += "&{attr}={value}".format(attr=i, value=kwargs[i])

        stdata = parse_urls(self.datahub.server, 
                            self.datahub.version, 
                            requrl,
                            self.datahub.apikey, **kwargs)

        return stdata.r.json()

    def get_station_data_as_pandas(self, station_list, count=1000, variables='temperature', start=(datetime.datetime.today() - datetime.timedelta(days=30)).strftime("%Y-%m-%dT00:00:00"),end=None):
        if end == None:
            end = (datetime.datetime.strptime(start,"%Y-%m-%dT%H:%M:%S") + datetime.timedelta(days=30)).strftime("%Y-%m-%dT00:00:00")
        """
        Get station list as input and return properly formatted dataframe
        Columns, station ID/var
        """
        def l1(ind):
            return [ind[j] for j in variables]
        variables = [variables,] if type(variables) == str else variables
        tempdata = {}
        for i in station_list:
            dd = self.get_station_data(count=count, stations=i, variables=",".join(variables), start = start)
            if 'entries' in dd:
                ab = list(zip(*[[i['axes']['time'], l1(i['data'])] for i in dd['entries']]))
            else:
                dd = self.get_station_data(count=count, stations=i, variables=",".join(variables), start = start)
                ab = list(zip(*[[i['axes']['time'], l1(i['data'])] for i in dd['entries']]))
#            print(len(dd['entries']))
            if ab:
                tempdata[i] = pd.DataFrame(list(ab[1]),
                                           index=pd.to_datetime(ab[0]),
                                           columns=variables)
            # for tval in dd['entries']:
            #     for vv in variables:
            #         tempdata[i][vv].append((parse(tval['axes']['time']),tval['data'][vv]))
        return tempdata

    def get_subdatasets(self):
        return parse_urls(self.datahub.server,self.datahub.version,"datasets/"+self.datasetkey+"/subdatasets",self.datahub.apikey).r.json()['subdatasets']

    def get_reftimes(self):
        subdatasets = self.get_subdatasets()
        self.reftimes=list(map(lambda x: datetime.datetime.utcfromtimestamp(x/1e3), 
                           sorted(set(itertools.chain.from_iterable(
                                  [[i['referenceTimeCoverage']['start'],
                                    i['referenceTimeCoverage']['end']] for i in subdatasets])))))

    def get_timesteps(self):
        subdatasets = self.get_subdatasets()
        self.timesteps=list(map(lambda x: datetime.datetime.utcfromtimestamp(x/1e3), 
                           sorted(set(itertools.chain.from_iterable(
                                  [[i['temporalCoverage']['start'],
                                    i['temporalCoverage']['end']] for i in subdatasets])))))

    def get_dataset_boundaries(self):
        boundaries=parse_urls(self.datahub.server,self.datahub.version,"datasets/"+self.datasetkey,self.datahub.apikey)
        rj = boundaries.r.json()['SpatialExtent']
        if rj['type'] == 'Polygon':
            rdict = rj['coordinates'][0]
        elif rj['type'] == 'MultiPolygon':
            rdict = rj['coordinates'][0][0]
        else:
            rdict = rj
        return rdict

