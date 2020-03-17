import pandas as pd
import pytz
from datetime import date
from datetime import datetime
from datetime import timedelta

def get_start_date(flight_date, timezone):
    #date object for the flight date
    flight_date_object = datetime.strptime(flight_date, '%Y-%m-%d')
    #append the midnight time to the flight date - this will be the start of the periond given for flights shedules API
    flight_date_midnight = datetime.combine(flight_date_object, datetime.min.time())
    #the timezone object of the origin airport
    origin_tzn = pytz.timezone(timezone)
    #timezone aware flight datetime
    aware_start_date = origin_tzn.localize(flight_date_midnight)
    #convert the date to the unix timezone
    unix_start_date = aware_start_date.astimezone(pytz.timezone('UTC'))
    #return in timestamp format
    return int(unix_start_date.timestamp())

def get_end_date(start_unix_timestamp):
    #add one day to get the end of the search period
    tdelta = timedelta(days=1)
    timestamp = datetime.fromtimestamp(start_unix_timestamp)
    unix_end_date = timestamp + tdelta
    return int(unix_end_date.timestamp())

def get_unix_dates(input_df):
    input_df['StartUnixDate']=input_df.apply(lambda x: get_start_date(x['Flight Date Str'], x['TimeZone']), axis=1)
    input_df['EndUnixDate']=input_df.apply(lambda x: get_end_date(x['StartUnixDate']), axis=1)
    return input_df

