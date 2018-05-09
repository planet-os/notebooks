# -*- coding: utf-8 -*-

import datahub
from lib.dataset import dataset


def test_stations_exist():
    apikey = open("APIKEY").read().strip()
    dh = datahub.datahub(server='dpipe-api.staging04.planetos.com', version='api/v1',apikey=apikey)
    ds = dataset('synop_timeseries_test',dh)
    dss = ds.stations()
    assert 'errors' not in dss
    ds2 = dataset('metno_wind_test',dh)
    dss2 = ds2.stations()
    assert 'errors' in dss2


