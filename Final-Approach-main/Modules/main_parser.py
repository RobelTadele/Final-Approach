import sys, math, os, pickle, message
from message import popUpError
import pandas as pd
import matplotlib as plt
import numpy as np
from tkinter import *
from grapher import graph_mapper
from grapher import entity

# Main
def main():

    # Read in User Selected Paths from Pickle 
    with open('Modules/Caches/directories.pkl', 'rb') as file:
        csv_set = pickle.load(file)
   
    entities = []
    for csv_path in csv_set:
        
        # Creating Pandas DataFrame
        parsed_data = load_raw_data(csv_path)
       
        # Detect when Landing occurs
        indexes = detect_landing(parsed_data, csv_path)

        if indexes == False: continue

        # Parsed Data columns : 0. Airspeed, 1. longitude, 2. latitude, 3. altitude, 4. Time
        landing_altitudes = gather_altitude(parsed_data[3], indexes)
        
        # calc[0], calc[1], calc[2] = speed ranges, avg speed, dict of coordinates
        calc = calculator(parsed_data, indexes)
        
        entities.append(entity(csv_path, calc[1], calc[2]))

        # ! Test Zone
        # with open('dump.txt', 'a') as file:
        #     file.write('File Name = ' + csv_path + '\n' + 'Landing Altitudes : ')
        #     for i in landing_altitudes: file.write(str(i) + ' ')
        #     file.write("\n\nSpeed Ranges\n")
        #     for k,v in calc[0].items(): file.write(f'{k} : {v}' + '\n')
        #     file.write("\nAverage Speeds between ranges\n")
        #     for k,v in calc[1].items(): file.write(f'{k} : {v}' + '\n')
        #     file.write("\nCoordinates (x,y)\n")
        #     for k,v in calc[2].items(): file.write(f'{k} : {v}' + '\n')
        #     file.write('\n---------------------------------------------------------------------\n')
         # ! Test Zone
        
    # Initialize graph mapper with list of entitiy objects
    x = graph_mapper(entities)

    # Graph Data inside Entities
    x.main()

    #! If landing happens at midnight give pop up message to let user know flight exists in two separate flights

def calculator(data_source, indexes):
    '''Calculates Average Speed of Flights from range 200-50ft in 50ft increments\n
    returns dict like {'200-150': [66.4, 67.3, 68.7, 69.3, 70.1], '150-100': [67.9, 67.0, 65.7, 64.8, 64.1], '100-50': [63.8, 63.1, 62.6, 62.6, 62.7]},
    {'200-150': 45.3,'150-100': 23.3, '100-50': 58.2}
    '''

    from_index = indexes[0]
    airspeed, altitude = data_source[0], data_source[3]
    long, lat = data_source[1], data_source[2]

    #! Need to do one pass to check if plane drops below 54 knts more than once and return False
    #! if it does so file will be skipped


    # Storing Average Speed between ranges
    avg_speed = {}
    speed_range = {'200-150': [],'150-100': [], '100-50':[]}
    cords_range = {'200-150': [],'150-100': [], '100-50':[]}

    # Can be optimized
    to_pointer = 0 + from_index

    while altitude[to_pointer] >= (altitude[to_pointer] - 50):
        if (altitude[from_index] - altitude[to_pointer]) >= 50:
            break
        speed_range['200-150'].append(airspeed[to_pointer])
        cords_range['200-150'].append((long[to_pointer], lat[to_pointer]))

        to_pointer+=1

    from_index = to_pointer
    while altitude[to_pointer] >= (altitude[to_pointer] - 50):
        if (altitude[from_index] - altitude[to_pointer]) >= 50:
            break
        speed_range['150-100'].append(airspeed[to_pointer])
        cords_range['150-100'].append((long[to_pointer], lat[to_pointer]))

        to_pointer+=1

    from_index = to_pointer
    while altitude[to_pointer] >= (altitude[to_pointer] - 50):
        if (altitude[from_index] - altitude[to_pointer]) >= 50:
            break
        speed_range['100-50'].append(airspeed[to_pointer])
        cords_range['100-50'].append((long[to_pointer], lat[to_pointer]))

        to_pointer+=1

    
    for k,v in speed_range.items():
        avg_speed[k] = (sum(v)/len(v))
   
    return speed_range, avg_speed, cords_range
        
def gather_altitude(alt, indexes) -> list:
    '''Grabs Flight parameters from CSV Using Indexes where landings have been identified'''
    
    from_index, to_index = indexes[0], indexes[1]
    to_index += 1

    altitude = alt
    final_altitude = altitude[from_index:to_index]

    return final_altitude
    
def detect_landing(parsed_data, csv_path) -> int:
    '''Detects when airpseed drops below 51knts, while altitude is declining, and plane is within 'ground level'
        \nReturns index ranges for landings eg: 2989 3016'''
    row_size = len(parsed_data[0])
    
    indicated_Airspeed, time = parsed_data[0], parsed_data[4]
    longitude, latitude, altitude = parsed_data[1], parsed_data[2], parsed_data[3]
    
    for i in range(row_size):

        # If indicated_Airspeed, longitude, latitude, or latitude is missing row skip iteration
        if pd.isna(indicated_Airspeed[i]) or pd.isna(longitude[i]) or pd.isna(latitude[i]) or pd.isna(latitude[i]):
            continue

        # If indicated_airspeed (IAS) is not between 48 and 54
        if not (48 < indicated_Airspeed[i] < 54) :
            continue

        # BackTrack and find if plane is at realtively the same altitude or accelerating
        if (altitude[i-30] - altitude[i]) < 15:
            continue

        # Firts index where IAT is between 48 and 54
        from_index = i
        break
    try: 
        # Touchdown Altitude
        landing_altitude = altitude[from_index]

        # determining how far to backtrack
        to_index = 0 + from_index
        
        # Keep going back until altitude is greater than 200 from landing altitude 
        while True:
            from_index -= 1
            if altitude[from_index] > landing_altitude + 200:
                break
    except:
        print(f'Invalid File skipped: {csv_path} ')
        return False
    
    return from_index, to_index

def load_raw_data(csv_path) -> list:
    '''Loading raw CSV from directory
    returns columns : Airspeed, longitude, latitude, altitude, time
    '''
    # Columns to be read from CSV from row 3 (contains header info)
    column_list = ['UTC Time','Latitude','Longitude','AltGPS','IAS']
    
    try:
        df = pd.read_csv(csv_path, header=2, usecols=column_list)
        time = df['UTC Time']
        airspeed = df['IAS']
        longitude = df['Longitude']
        latitude = df['Latitude']
        altitude = df['AltGPS']
        
    except Exception as ex:
        popUpError('CSV Failed to Load')
        sys.exit()
    
    return to_list(airspeed),to_list(longitude), to_list(latitude), to_list(altitude), to_list(time)

def to_list(columnName:str) -> list:
    '''Returns Column values as a list'''
    return [i for i in list(columnName.values)]

if __name__ == '__main__':
    main()