#!/usr/bin/env python3
import matplotlib.pyplot as plt
from shapely.geometry.polygon import Polygon
from apiclient.dataset import dataset
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import json
import urllib.request
import numpy as np


def dataset_coverages(dh, savefig=False):
    mf_dataset = dataset('meteofrance_arome_001_surface',dh)
    nam_conus_dataset = dataset('noaa_nam_conusnest',dh)
    knmi_dataset = dataset('knmi_harmonie_europe',dh)
    #metno_harmonie_dataset = dataset('metno_harmonie_metcoop',dh)

    knmi_coverage = Polygon(knmi_dataset.get_dataset_boundaries())
    #era5_coverage = Polygon(era5_dataset.get_dataset_boundaries())
    mf_coverage = Polygon(mf_dataset.get_dataset_boundaries())
    nam_coverage = Polygon(nam_conus_dataset.get_dataset_boundaries())

    x_knmi,y_knmi = knmi_coverage.exterior.xy
    x_mf,y_mf = mf_coverage.exterior.xy
    x_nam,y_nam = nam_coverage.exterior.xy

    fig = plt.figure(figsize=(6,3))
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.coastlines()
    ax.stock_img()
    ax.add_feature(cfeature.BORDERS)
    ax.plot(x_knmi, y_knmi, color='#7CFC00', alpha=0.7,
            linewidth=3, solid_capstyle='round')
    ax.plot(x_mf, y_mf, color='#ffff00', alpha=0.7,
            linewidth=3, solid_capstyle='round')

    ax.plot(x_nam, y_nam, color='grey', alpha=0.7,
        linewidth=3, solid_capstyle='round')
    if savefig:
        plt.savefig('presentation_model_areas', bbox_inches='tight')
    plt.show()


# def dataset_resolutions():
#     fera5 = xr.open_dataset('ERA53.nc')
#     fknmi = xr.open_dataset('KNMI3.nc')
#     fig = plt.figure()
#     levels = np.arange(-10, 13, 0.2)
#     ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
#     fera5.eastward_wind_at_10_metres.isel({'time0':0}).plot(ax=ax, cmap=plt.cm.jet, levels=levels)
#     bounds = [0,7,50,55]
#     ax.set_extent(bounds)
#     ax.add_feature(cfeature.COASTLINE)
#     ax.add_feature(cfeature.BORDERS, linestyle=':')

#     fig = plt.figure()
#     ax2 = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
#     fknmi.u_wind_height_above_ground.isel({'time':0}).plot(ax=ax2, cmap=plt.cm.jet, levels=levels)
#     ax2.set_extent(bounds)
#     ax2.add_feature(cfeature.COASTLINE)
#     ax2.add_feature(cfeature.BORDERS, linestyle=':')
#     plt.show()


def _generate_raster_api_query(server, dataset_key, longitude_west,
                               latitude_south, longitude_east,
                               latitude_north, count, API_key, **kwargs):
    returl = server + dataset_key + "/area?apikey={0}&polygon=[[{1},{3}],[{2},{3}],[{2},{4}],[{1},{4}],[{1},{3}]]&grouping=location&count={5}&reftime_recent=true".format(
        API_key,longitude_west,longitude_east,latitude_south,latitude_north,count)
    for i,j in kwargs.items():
        returl += "&{0}={1}".format(i,j)
    print(returl)
    return returl


def read_raster_data_to_json(server, dataset_key, longitude_west,
                               latitude_south, longitude_east,
                               latitude_north, count, API_key, **kwargs):
    return json.loads(urllib.request.urlopen(_generate_raster_api_query(server, dataset_key, longitude_west,
                               latitude_south, longitude_east,
                               latitude_north, count, API_key, **kwargs)).read().decode('utf-8'))['entries']

def dataset_resolutions(API_key):
    bounds = [2,7,52,55]
    server="http://api.planetos.com/v1/datasets/"
    knmi_u=read_raster_data_to_json(
            server,
            'knmi_harmonie_europe',
            bounds[0],
            bounds[2],
            bounds[1],
            bounds[3],
            1, API_key,var='u_wind_height_above_ground',reftime_start='2021-01-01T00:00:00', time='2021-01-01T01:00:00')[0]

    era5_u = read_raster_data_to_json(
            server,
            'ecmwf_era5_v2',
            bounds[0],
            bounds[2],
            bounds[1],
            bounds[3],
            1, API_key,var='eastward_wind_at_10_metres',
            time_start='2021-01-01T01:00:00')[0]

    vmin = np.amin([
        np.amin(knmi_u['data']['u_wind_height_above_ground']),
        np.amin(era5_u['data']['eastward_wind_at_10_metres'])]
                   )
    vmax = np.amax([
        np.amax(knmi_u['data']['u_wind_height_above_ground']),
        np.amax(era5_u['data']['eastward_wind_at_10_metres'])]
                   )
    longitudes, latitudes = np.meshgrid(knmi_u['indexAxes'][1][1], knmi_u['indexAxes'][0][1])
    era5_lon, era5_lat = np.meshgrid(era5_u['indexAxes'][1][1], era5_u['indexAxes'][0][1])
    fig=plt.figure(figsize=(6,3))
    ax = fig.add_subplot(1, 2, 1, projection=ccrs.PlateCarree())
    ax.pcolormesh(longitudes, latitudes, knmi_u['data']['u_wind_height_above_ground'],
              vmin=vmin, vmax=vmax)
    ax.title.set_text("KNMI HARMONIE")
    ax.coastlines()
    ax=fig.add_subplot(1, 2, 2, projection=ccrs.PlateCarree())
    ppp=ax.pcolormesh(era5_lon, era5_lat, era5_u['data']['eastward_wind_at_10_metres'],
              vmin=vmin, vmax=vmax)
    ax.coastlines()
    ax.title.set_text("ERA5")
    plt.show()
