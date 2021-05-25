import datetime
from pick import pick
from apiclient.predef_locations import locations
import dateutil.parser


class variable:
    def __init__(self, varname, input_variables, scope, ds, debug=False):
        self.varname = varname
        self.ds = ds
        var_attrs = [i for i in input_variables if i['variableKey'] == varname]
        var_attrs = var_attrs[0]
        if 'temporalCoverage' in var_attrs:
            for at in ['start','end']:
                setattr(self, at, datetime.datetime.utcfromtimestamp(var_attrs['temporalCoverage'][at]/1e3))
        for at in ['units','long_name']:
            if at in var_attrs:
                setattr(self, at, var_attrs[at])
        for sc in scope:
            setattr(self, sc, scope[sc])
        self.values = {}
        self.debug = debug

    ## This does not work in notebook mode...
    def get_values_interactive(self):
        selected_reftime    = pick(self.reftimes, "select reftime: ", multi_select=True, min_selection_count=1)
        selected_start_time = pick(self.timesteps, "select start", min_selection_count=0)
        selected_end_time   = pick(self.timesteps, "select end", min_selection_count=0)
        locations.update({'other':'lon,lat'})
        selected_coords = pick(list(locations.keys()), 'select location or insert custom', min_selection_count=1)
        selected_count = pick([1,10,100,1000,10000], 'count', min_selection_count=1)
#        print("selected coordinates", selected_coords)
        if selected_coords[0][0] == 'other':
            selected_lon = input("insert lon")
            selected_lat = input("insert lat")
            assert selected_lon >= -180
            assert selected_lon <= 360
            assert selected_lat <= 90
            assert selected_lat >= -90
        else:
            selected_lon = locations[selected_coords[0]][0]
            selected_lat = locations[selected_coords[0]][1]
            
        print("Is this correct:")
        print("reftime:", selected_reftime)
        print("start:", selected_start_time)
        print("end:", selected_end_time)
        assert input("y/n: ") == "y"
        start_time = selected_start_time[0]
        self.values['testloc'] = self.ds.get_json_data_in_pandas(debug=self.debug, **{'reftime_start':selected_reftime[0][0].isoformat(), 
                                                         'reftime_end':selected_reftime[-1][0].isoformat(), 
                                                         'vars':self.varname,
                                                         'lon':selected_lon,'lat':selected_lat,
                                                         'count':selected_count[0]})

    def get_values(self, location="Võru", reftime=None, reftime_end=None, count=10, debug=False):
        kwags = {}
        if not reftime:
            if self.reftimes:
                kwags['reftime_start'] = selected_reftime = self.reftimes[-1]
        else:
            kwags['reftime_start'] = reftime
        if reftime_end:
            kwags['reftime_end'] = reftime_end
        kwags['lon'] = locations[location][0]
        kwags['lat'] = locations[location][1]
        kwags['count'] = count
        kwags['vars'] = self.varname

        self.values[location] = self.ds.get_json_data_in_pandas(debug=debug, **kwags)
## **{'reftime_start':selected_reftime.isoformat(),
                                   ## 'reftime_end':reftime_end.isoformat(), 
                                   ## 'vars':self.varname,
                                   ## 'lon':selected_lon,'lat':selected_lat,
                                   ## 'count':selected_count})
                                

class variables:
    def __init__(self, input_variables, scope, ds, debug=False):
        for i in input_variables:
            varname = i['variableKey']
            setattr(self, varname.replace('-',''), variable(varname, input_variables, scope, ds))
