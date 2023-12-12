import numpy as np
import pandas as pd
import os
np.random.seed(1234)

import tensorflow as tf
from tensorflow import keras
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

from datetime import datetime, timedelta
from sklearn.metrics import r2_score, mean_squared_error
import matplotlib.pyplot as plt

stID = {
        155 : ['COMOX A', 1953, 2023],
        6781: ['HOPEDALE (AUT)', 1953, 2023],
        6354: ['GREENWOOD A', 1953, 2023],
        3987: ['ARMSTRONG (AUT)', 1953, 2023],
        5126: ['TRENTON A', 1953, 2023],
        2832: ['COLD LAKE A', 1954, 2023],
#         1739: ['CAPE DYER', 1955, 2023],
        1633: ['CAPE PARRY A', 1956, 2023],
        3649: ['PILOT MOUND (AUT)', 1957, 2023],
        1556: ['HAINES JUNCTION', 1960, 2023]
        }

targets = ['Max Temp (°C)', 'Min Temp (°C)', 'Mean Temp (°C)', 'Total Rain (mm)', 'Total Snow (cm)', 'Total Precip (mm)']

for stationID, j in stID.items():#155: ['COMOX A', 1953, 2023], 6781: ['HOPEDALE (AUT)', 1953, 2023]}.items():
    print(f'\nStarting process for {j[0]}\n')
    
    fpath = f'data/Daily_{j[0]}_{stationID}.csv'
    
    dfc = pd.read_csv(fpath)[['Longitude (x)', 'Latitude (y)', 'Station Name', 'Date/Time', \
                              'Max Temp (°C)', 'Min Temp (°C)', 'Mean Temp (°C)', \
                              'Total Rain (mm)', 'Total Snow (cm)', 'Total Precip (mm)']]
    
    dfs = dfc.copy()
    missing_dates = pd.Series(pd.date_range(start = dfs['Date/Time'].min(), \
                                            end = dfs['Date/Time'].max()).difference(dfs['Date/Time'])).astype(str)
    dfs = pd.concat([dfs, pd.DataFrame({'Date/Time': missing_dates})])
    dfs['Date/Time'] = pd.to_datetime(dfs['Date/Time'])
    dfs.sort_values('Date/Time', inplace=True)
    data = dfs.interpolate('ffill')
    data[targets] = data[targets]._convert(numeric=True)

    zz = pd.DataFrame(columns=['Station Name','Date/Time'])
    zzz = data.copy()
    
    # Forecasting starts keeping one target at a time
    for target in targets:
        print(f'Starting predictions for {target}')
        
        # Creating sequences
        sequence_length = 365
        data_sequences = []
        target_data = []

        for i in range(len(data) - sequence_length):
            data_sequences.append(data[target].values[i:i+sequence_length])
            target_data.append(data[target].values[i+sequence_length])

        data_sequences = np.array(data_sequences)
        target_data = np.array(target_data)

        X_train, X_val, y_train, y_val = train_test_split(data_sequences, target_data, test_size=0.1, shuffle=False, random_state=1234)
        
        # Modelling
        print('Modelling starting...')
        model = keras.Sequential()
        model.add(keras.layers.LSTM(64, input_shape=(sequence_length, 1)))
        model.add(keras.layers.Dense(1))
        model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])
        model.fit(data_sequences, target_data, epochs=10, batch_size=61, validation_data=(X_val, y_val))
        
        
        # Future predictions (1 year)
        n_future_steps = 365
        last_sequence = data[target].values[-sequence_length:]
        extended_sequence = last_sequence.copy()

        for i in range(n_future_steps):
            try:
                sequence = extended_sequence[-sequence_length:].reshape(1, sequence_length, 1)
                next_prediction = round(model.predict(sequence),1)
                extended_sequence = np.append(extended_sequence, next_prediction)
            
            except:
                if len(extended_sequence)==n_future_steps: continue
                else: print(f'ERROR in {j[0]}')
                break

        predicted_future = extended_sequence[-n_future_steps:]        
        future_timestamps = pd.date_range(start=max(data['Date/Time']), periods=n_future_steps + 1, closed='right')
        predicted_future_df = pd.DataFrame(index=future_timestamps, data={'predictions': predicted_future})
        
        # expanding dataframe
        z = predicted_future_df.reset_index()
        z.columns = ['Date/Time', target]
        z['Station Name'] = j[0]
        
        zz = pd.merge(zz, z, on=['Station Name','Date/Time'], how='outer')
#         display(zz)
        zzz = pd.concat([zzz, zz], ignore_index=True)
    
    zzz['Latitude (y)'] = data['Latitude (y)'].mode()[0]
    zzz['Longitude (x)'] = data['Longitude (x)'].mode()[0]

    zzz = zzz.groupby(by=['Longitude (x)', 'Latitude (y)', 'Station Name', 'Date/Time']).mean().reset_index()

    os.makedirs('forecast/', exist_ok =True)
    zzz.to_csv(f'forecast/forecast_{j[0]}_{stationID}.csv', index=False)