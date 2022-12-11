import pandas as pd 
from datetime import datetime
import os
# UTC OFFset
directories= {
        'direct': "CitabriaData",
        'parentFolder':"Partitioned_Data",
        'headerCache': 'Modules/Caches/headerInfo.csv',
        'date_partitions': 'Partitioned_Data'
    }

def split_by_flight(fileName, header):
    df = pd.read_csv(fileName, skiprows=2)
    utc = df['UTC Time']
    headPointer = 0

    for i in range(len(utc)-1):
        
        top = datetime.strptime(utc[i], "%H:%M:%S")
        bottom = datetime.strptime(utc[i+1], "%H:%M:%S")
        delta = bottom - top
        
        # Time Difference is more than 5 minutes
        if delta.total_seconds()/60 >= 5:
            name = f'{utc[headPointer]}-{top.time()}'.replace(":", '_')
            
            x = f'Partitioned_Data/Individual/temp {name}.csv'
            print(f'New Flight: {top.time()}, Delta: {delta}')

            header.to_csv(x,index=True, header=True)
            df[headPointer:i+1].to_csv(x, mode='a', index=False)
            headPointer = i+1
          
def main():
    location = r'Partitioned_Data\2020\10\02\Citabria_2020-10-02 4JQ006168 (1).csv'

    dfheader = pd.read_csv(location)[:1]
    dfheader.to_csv(directories['headerCache'], header=None)

    # Read parent data, skipping first two rows
    df = pd.read_csv(location, skiprows=2)

    # Adding Airfram Name Column
    dfheader['airframe_name = "ACA7ECA"'] = ""

    split_by_flight(location, dfheader)

if __name__ == '__main__':
    main()