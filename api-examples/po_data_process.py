
import urllib.request
import simplejson as json
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
import numpy
import matplotlib.gridspec as gridspec
import datetime
import numpy as np
import matplotlib as mpl
from matplotlib.ticker import MultipleLocator
mpl.rcParams['font.size'] = 16

server = "http://api.planetos.com/v1/datasets/"
def generate_point_api_query(dataset_key, longitude, latitude, API_key, count=100000, z='all',verbose = 'False', **kwargs):
    server = "http://api.planetos.com/v1/datasets/"
    returl = server + dataset_key + "/point?lat={0}&lon={1}&apikey={2}&count={3}&z={4}&verbose={5}".format(latitude,longitude,API_key,count,z,verbose)
    for i,j in kwargs.items():
        returl += "&{0}={1}".format(i,j)
    return returl

def generate_raster_api_query(dataset_key,server, longitude_west, latitude_south, longitude_east, latitude_north, API_key,count=100, **kwargs):
    returl = server + dataset_key + "/area?apikey={0}&polygon=[[{1},{3}],[{2},{3}],[{2},{4}],[{1},{4}],[{1},{3}]]&grouping=location&count={5}&reftime_recent=true".format(API_key,longitude_west,longitude_east,latitude_south,latitude_north,count)
    for i,j in kwargs.items():
        returl += "&{0}={1}".format(i,j)
    return returl

def read_data_to_json(req_url):
    return json.loads(urllib.request.urlopen(req_url).read().decode('utf-8'))


def download_netcdf_file(query):
    status = requests.get(query,stream = True)
    #This one need to be completed later! 

def convert_json_to_some_pandas(injson):
    param_list = ['axes','data']
    new_dict = {}
    [new_dict.update({i:[]}) for i in param_list]
    [(new_dict['axes'].append(i['axes']),new_dict['data'].append(i['data'])) for i in injson];
    pd_temp = pd.DataFrame(injson)
    dev_frame = pd_temp[['context','axes']].join(pd.concat([pd.DataFrame(new_dict[i]) for i in param_list],axis=1))
    return dev_frame

def get_units(dataset_key, variable,API_key):
    query = server +'{0}/variables?apikey={1}&variables={2}'.format(dataset_key,API_key,variable)
    json = read_data_to_json(query)['variables']
    attributes = [u['attributes'] for u in json][0]
    uns = [v['attributeValue'] for v in attributes if v['attributeKey'] == 'units'][0]
    return uns

def get_data_from_point_API(dataset_key, longitude, latitude, API_key):
    
    data = convert_json_to_some_pandas(read_data_to_json(generate_point_api_query(dataset_key, longitude, latitude, API_key))['entries'])
    return data

def get_data_from_raster_API(dataset_key, longitude, latitude, API_key):
    
    data = convert_json_to_some_pandas(read_data_to_json(generate_raster_api_query(dataset_key,server, longitude_west, latitude_south, longitude_east, latitude_north, API_key))['entries'])
    return data

def get_data_in_pandas_dataframe(dataset_key, longitude, latitude, API_key):
    data = get_data_from_point_API(dataset_key, longitude, latitude, API_key)
    data['time'] = pd.to_datetime(data['time'])
    data['year'] = data['time'].dt.year
    data['month'] = data['time'].dt.month
    now = datetime.datetime.now()
    data = data.loc[data['year'] < now.year] 
    print (data.keys())
    return data

def make_plot(data,dataset_key1,title,**kwargs):
    fig = plt.figure(figsize=(15,5))
    try:
        data_time = data['time.year']
    except:
        try:
            data_time = data.year
        except:
            data_time = None
            
    if data_time is not None:
        if 'trend' in kwargs:
            z = numpy.polyfit(data_time, data, 1)
            p = np.poly1d(z)
            plt.plot(data_time,p(data_time),"r--",c='green')
            
        plt.plot(data_time,data, '*-',linewidth = 1,c='blue',label = dataset_key1) 
    else:
        plt.plot(data, '*-',linewidth = 1,c='blue',label = dataset_key1) 

    #plt.plot(data, '*-',linewidth = 1,c='blue',label = dataset_key1) 
    #plt.xlabel('Time')
    plt.title(title)
    plt.grid()
    ml = MultipleLocator(1)
    bl = MultipleLocator(10)
    plt.axes().xaxis.set_minor_locator(ml)
    plt.axes().xaxis.set_major_locator(bl)

    #plt.minorticks_on()
    if len(kwargs) > 0:
        if 'dataset_key2' and 'data2' in kwargs:
            plt.plot(kwargs['data2'], '*-',linewidth = 1,c='red',label = kwargs['dataset_key2']) 
            plt.legend()
        if 'ylabel' in kwargs:
            plt.ylabel(kwargs['ylabel'])
        if 'xlabel' in kwargs:
            plt.ylabel(kwargs['xlabel'])
        if 'compare_line' in kwargs:
            plt.plot([np.min(data_time).values-2,np.max(data_time).values+2],[kwargs['compare_line'],kwargs['compare_line']],':',c='red',linewidth=1.5)
    fig.autofmt_xdate()
    plt.xticks(rotation = 0)
    #plt.savefig('plot_out' + title + '.png', dpi=300)
    plt.show()

def running_mean(x, N):
    cumsum = numpy.cumsum(numpy.insert(x, 0, 0)) 
    return (cumsum[N:] - cumsum[:-N]) / N 

def make_histogram(data,bins):
    fig, ax = plt.subplots()
    plt.hist(data,bins=bins,rwidth = 0.98)
    plt.xscale('log')
    ax.set_xticks(bins)
    ax.xaxis.set_major_formatter(ScalarFormatter())
    plt.show()

def get_comparison_graph(lon1,lat1,data1,lon2,lat2,data2,title):
    vmax = numpy.max([numpy.max(data1),numpy.max(data2)])
    vmin = numpy.min([numpy.min(data1),numpy.min(data2)])

    gs1 = gridspec.GridSpec(1, 2)
    gs1.update(wspace=0.25)
    fig = plt.figure(figsize = (6,4))
    fig.subplots_adjust(wspace=0.3, hspace=0.4, right=0.8)
    fig.suptitle(title)
    ax1 = fig.add_subplot(gs1[0])
    ax2 = fig.add_subplot(gs1[1])


    c1 = ax1.pcolormesh(lon1,lat1,data1,vmin = vmin,vmax = vmax)
    c2 = ax2.pcolormesh(lon2,lat2,data2,vmin = vmin,vmax = vmax)
    
    bbox = ax2.get_position()
    cbar_loc = fig.add_axes([bbox.xmax * 1.03, bbox.ymin + 0.01, bbox.width*0.06, bbox.height - 0.025])

    plt.colorbar(c2,cax = cbar_loc)
    plt.show()

def comparison_bar_chart(data1,area_name1, data2,area_name2,xaxis_label, xtick_range,yaxis_label,title):
    fig = plt.figure(figsize=(20,5))
    ax = fig.add_subplot(111)
    bar_width = 0.35
    opacity = 0.4
    ax.bar(np.arange(0,len(data1),1)-bar_width/2,data1,
           bar_width,
           color='#00FF00',
           label = area_name1)
    ax.bar(np.arange(0,len(data2),1)+bar_width/2,data2,
           bar_width,
           color='orange',
           label = area_name2)
    plt.setp(ax, xticks = np.arange(0,len(data1),1),
             xticklabels=xtick_range)
    #plt.xticks()
    plt.xlabel(xaxis_label,fontsize=16)
    plt.ylabel(yaxis_label,fontsize=16)
    plt.grid()
    plt.title(title,fontsize=20)
    plt.legend(fontsize=16)
    #plt.savefig('barchart_out.png',dpi=300)
    plt.show()

def make_comparison_plot(data1,area_name1,data2,area_name2,title,**kwargs):
    fig = plt.figure(figsize=(20,5))
    ax = fig.add_subplot(111)
    try:
        ax.plot(data1.year,data1,'-*',label = area_name1,color = '#00FF00')
        ax.plot(data2.year,data2,'-o',label = area_name2,color = 'orange')
    except AttributeError:
        try:
            ax.plot(data1.time1[:],data1,'-*',label = area_name1,color = '#00FF00')
            ax.plot(data2.time1[:],data2,'-o',label = area_name2,color = 'orange')
        except AttributeError:
            ax.plot(data1.time[:],data1,'-*',label = area_name1,color = '#00FF00')
            ax.plot(data2.time[:],data2,'-o',label = area_name2,color = 'orange')

    if 'xaxis_label' in kwargs:
        plt.xlabel(kwargs['xaxis_label'])
    if 'yaxis_label' in kwargs:
        plt.ylabel(kwargs['yaxis_label'])
    plt.grid()
    plt.legend()
    plt.minorticks_on()
    plt.title(title)    

def make_anomalies_plot(data,threshold,title,**kwargs):
    fig = plt.figure(figsize=(15,5))
    minus_mask = np.where((data) < threshold)
    plus_mask = np.where((data) > threshold)
    plt.bar(data['time.year'][minus_mask],(data)[minus_mask], color = 'blue')
    plt.bar(data['time.year'][plus_mask],(data)[plus_mask],color = 'red')
    if 'xaxis_label' in kwargs:
        plt.ylabel(kwargs['xaxis_label'])
    if 'yaxis_label' in kwargs:
        plt.ylabel(kwargs['yaxis_label'])
    ml = MultipleLocator(1)
    bl = MultipleLocator(10)
    plt.axes().xaxis.set_minor_locator(ml)
    plt.title(title,fontsize=20)
    plt.axes().xaxis.set_major_locator(bl)
    title = title.replace('.','_')
    #plt.savefig('anomaly_out_' + title +'.png',dpi=300)
    plt.show() 