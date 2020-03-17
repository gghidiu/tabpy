# the timezone is necesary to get timezone aware times which can be converted to unix timestamps
import pandas as pd
from timezonefinder import TimezoneFinder

def get_timezone(longitude, latitude):
    tf = TimezoneFinder()
    return tf.timezone_at(lng=longitude, lat=latitude)

def get_timezone_df(input_df):
    input_df['TimeZone']=input_df.apply(lambda x: get_timezone(longitude=x['Longitude1'],latitude=x['Latitude1']), axis=1)
    return input_df