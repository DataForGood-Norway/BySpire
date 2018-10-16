import re
import datetime
import pandas as pd

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


def sensor_csv_date_parser(s):
    patterns_to_try = ['%Y-%m-%d', '%d/%m/%Y',]
    for pattern in patterns_to_try:
        try:
            return datetime.datetime.strptime(s, pattern)
        except Exception as e:
            pass
    raise Exception("Unseen date format encountered!")
    return None


def sensor_csv_reader(fn):
    """
    A only just working csv loader that handles the formats we've seen so far...
    Tests etc when we want to productionize a fixed schema.
    """
    resp = {'FILENAME': fn, 'DF': None, 'DF_EXCEPTION': None}
    
    # assume there is a header
    try:
        df = pd.read_csv("../data/Measurements/"+fn)
        df['Date'] = df['Date'].apply(sensor_csv_date_parser)
        if list(df.columns) == list(sensor_csv_reader.default_schema[:len(df.columns)]):
            resp['DF'] = df
            resp['HEADER'] = True
            resp['NCOLS'] = len(df.columns)
            resp['NROWS'] = len(df)
            df['FILENAME'] = fn
            return pd.Series(resp)
    except Exception as e:
        pass

    # assume there isn't a header?
    try:
        ncols = len(pd.read_csv("../data/Measurements/"+fn, nrows=1).columns)
        assert ncols > 3  # catch some fringe cases :(
        df = pd.read_csv("../data/Measurements/"+fn,
                         names=sensor_csv_reader.default_schema[:ncols])
        df['Date'] = df['Date'].apply(sensor_csv_date_parser)
        resp['DF'] = df
        resp['HEADER'] = False
        resp['NCOLS'] = len(df.columns)
        resp['NROWS'] = len(df)
        df['FILENAME'] = fn
        return pd.Series(resp)
    except Exception as e:
        resp['DF_EXCEPTION'] = str(e)
    
    return pd.Series(resp)

sensor_csv_reader.default_schema = ['Date', 'Time', 'Air temp', 'Humidity', 'Water level', 'Water temp',
       'EC', 'pH', 'CO2', 'DO']


def sensor_time_parser(ts):
    """
    Most match a %H:%M:%S format, but some have :000 three digit seconds, 000-059
    """
    try:
        return datetime.datetime.strptime(ts, '%H:%M:%S').time()
    except Exception as e:
        pass
    try:
        return datetime.datetime.strptime(ts, '%H:%M:0%S').time()
    except Exception as e:
        pass
    return None
