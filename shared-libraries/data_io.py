import re
import datetime
YEAR_DEFAULT = 2018

def parse_sensor_filename(fn):
    """
    Reads sensor file names and returns a dictionary of attributes contained
    in the filename.
    
    e.g. 'Rack_4_20_09_1551.csv'
    """
    gd = None
    resp = {"FILENAME": fn}
    
    for pattern_name, pattern in parse_sensor_filename.patterns.items():
        matches = re.search(pattern, fn)
        if matches is not None:
            gd = matches.groupdict()
            resp['PATTERN_NAME'] = pattern_name
            break
    
    
    # no matches for any pattern, continue
    if gd is None:
        if fn[:-4].lower() == ".csv":
            print("csv error: ", fn)
        return resp
    
    # parse matches, this will be fragile!
    dt = datetime.datetime(YEAR_DEFAULT, int(gd['month']),
           int(gd['day']), int(gd['hour']), int(gd['minute']))
    
    resp["FILE_TIMESTAMP"] = dt
    resp["RACK"] = gd['rack'] if 'rack' in gd else None
    return resp

parse_sensor_filename.patterns = {
    '1': r'Rack_(?P<rack>[\d\.]+)[_-](?P<day>\d+)[_-](?P<month>\d+)[_-](?P<hour>\d\d)(?P<minute>\d\d).csv$',
    '2': r'byspireMonitoring[^\d]*(?P<day>\d+)[_-](?P<month>\d+)[_-](?P<hour>\d\d)(?P<minute>\d\d).csv$',
    '3': r'byspireMonitoring[^\d]*(?P<rack>[\d\.]+)[_-](?P<day>\d+)[_-](?P<month>\d+)[_-](?P<hour>\d\d)(?P<minute>\d\d).csv$',
}
