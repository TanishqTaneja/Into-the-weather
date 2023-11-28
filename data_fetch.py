import pandas as pd
import matplotlib.pyplot as plt

import re
from datetime import datetime, timedelta
from dateutil import rrule
from pathlib import Path
import os

from bs4 import BeautifulSoup
import requests

# Selected stations
stID = {
        155 : ['COMOX A', 1953, 2023],
        6781: ['HOPEDALE (AUT)', 1953, 2023],
        6354: ['GREENWOOD A', 1953, 2023],
        3987: ['ARMSTRONG (AUT)', 1953, 2023],
        5126: ['TRENTON A', 1953, 2023],
        2832: ['COLD LAKE A', 1954, 2023],
        1739: ['CAPE DYER', 1955, 2023],
        1633: ['CAPE PARRY A', 1956, 2023],
        3649: ['PILOT MOUND (AUT)', 1957, 2023],
        1556: ['HAINES JUNCTION', 1960, 2023]
        }

def get_data(stationID, year, month, by = 2):
   
    base_url = "http://climate.weather.gc.ca/climate_data/bulk_data_e.html?"
    
    if by==1:
        query_url = "format=csv&stationID={}&Year={}&Month={}&timeframe=1".format(stationID, year, month)
    
    elif by==2:
        query_url = "format=csv&stationID={}&Year={}&timeframe=2".format(stationID, year)
    
    api_endpoint = base_url + query_url
    
    return pd.read_csv(api_endpoint, skiprows=0)

# Daily Data
weather_data = pd.DataFrame()
by = 2
for stationID, j in stID.items():#{155: ['COMOX A', 1953, 2023]}.items():
    
    try:
        os.makedirs('data/', exist_ok =True)
        print(f"\n[{datetime.now()}] Retrieving weather data for station \t: {j[0]}")

        if by==1: fpath = f'data/Hourly_{j[0]}_{stationID}.csv'
        if by==2: fpath = f'data/Daily_{j[0]}_{stationID}.csv'

        my_file = Path(fpath)
        if my_file.is_file():
            print('expanding the exsiting file...')
            main_df = pd.read_csv(fpath, parse_dates=['Date/Time'], low_memory=False)
            start_date = main_df['Date/Time'].max()
            end_date = pd.to_datetime(datetime.today())

            if (pd.to_datetime(start_date) - pd.to_datetime(end_date)).days>-3:
                print(f'\nData file already up to date {j[0]}.')
                continue

        else:
            print('creating file from scratch...')
            start_date = datetime.strptime(f'jan{j[1]}', '%b%Y')
            end_date = datetime.strptime(f'dec{j[2]}', '%b%Y')

        frames = pd.DataFrame()

        for dt in rrule.rrule(rrule.MONTHLY if by==1 else rrule.YEARLY, dtstart=start_date, until=end_date):
            df = get_data(stationID, dt.year, dt.month, by)
            frames = pd.concat([df,frames])

            frames = frames[frames['Mean Temp (°C)'].notna()].copy()

        if my_file.is_file():
            frames = frames.combine_first(main_df)

        frames['Date/Time'] = pd.to_datetime(frames['Date/Time'], format='%Y-%m-%d')
        frames.sort_values('Date/Time', ignore_index=True)

        frames.to_csv(fpath)

        weather_data = pd.concat([weather_data,frames])
        print("\t\t\t\tFinal weather Dataframe Shape\t\t:", weather_data.shape)

    except Exception as e:
        print(f'\nFailed for StationID {stationID} because :\t{e}')
        continue