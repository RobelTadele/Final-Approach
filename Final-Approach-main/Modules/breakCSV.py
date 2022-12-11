# Classify and Split CSV file into smaller CSV's
import pandas as pd
import os, re
from os import listdir
from datetime import datetime


def main():
    directories= {
        'direct': "CitabriaData",
        'parentFolder':"Partitioned_Data",
        'headerCache': 'Modules/Caches/headerInfo.csv',
        'date_partitions': 'Partitioned_Data'
    }
    csv_path = os.listdir(directories["direct"])
 
    for files in csv_path:
        
        # If not CSV file Skip
        if files[-4:].lower() != '.csv' :
            continue
        location = f'{directories["direct"]}\{files}'
        
        # Extract header info from parent CSV and store
        dfheader = pd.read_csv(location, dtype=object)[:1]
        dfheader.to_csv(directories['headerCache'], header=None)

        # Read parent data, skipping first two rows
        df = pd.read_csv(location, skiprows=2, dtype=object)
        print(f'Processing {files}')

        # Adding Airfram Name Column
        dfheader['airframe_name = "ACA7ECA"'] = ""

        # Create Folder
        folder_names(df['UTC Date'], directories['parentFolder'])
       
        # Split and Store CSV by Date
        split_csv(df, directories['parentFolder'], dfheader)
    print("Processing Complete, proceed to Final Approach window")



# Will trim if flight goes past midnight, need a way to fix this
def split_csv(df, parentFolder, headerInfo) -> None: 
    '''Splits CSV and stores files in Directory by YYYY-MM-DD'''

    for flightDate, group in df.groupby('UTC Date'):

        counter = 1
        year, month, day = flightDate[:4], flightDate[5:7], flightDate[8:10]

        # Change Format of Date from yyyy/mm/dd to yyyy_mm_dd
        flightDate = "_".join(flightDate.split('/')) 
        
        # Extract Serial From header and append to file name
        serial = re.findall('"([^"]*)"', headerInfo.columns[-2])[0]

        src_direct = f'{parentFolder}\{year}\{month}\{day}'
        name = f'Citabria_{flightDate} {serial} ({counter})'
        
        location = f'{parentFolder}\{year}\{month}\{day}\Citabria_{flightDate} {serial} ({counter}).csv'

        # Export to CSV in respective directory, if file with same name exists adds numeric value to end
        while os.path.exists(location):
            counter+= 1
        
        # Export header from parent csv to children csv and append split group to same CSV
        headerInfo.to_csv(location, index=True, header=True)
        group.to_csv(location, mode='a', index=False)

        split_by_flight(src_direct, name, headerInfo)
        
def split_by_flight(src_direct, loc_name, header):
    df = pd.read_csv(f'{src_direct}\{loc_name}.csv', skiprows=2, dtype=object)
    utc = df['UTC Time']
    headPointer = 0

    for i in range(len(utc)-1):
        
        top = datetime.strptime(utc[i], "%H:%M:%S")
        bottom = datetime.strptime(utc[i+1], "%H:%M:%S")
        delta = bottom - top
        
        # Time Difference is more than 5 minutes
        if delta.total_seconds()/60 >= 5:
            name = f'{utc[headPointer]}-{top.time()}'.replace(":", '_')
            
            fileName = f'{src_direct}\{loc_name} - {name}.csv'
            # print(f'New Flight: {top.time()}, Delta: {delta}')

            header.to_csv(fileName,index=True, header=True)
            df[headPointer:i+1].to_csv(fileName, mode='a', index=False)
            headPointer = i+1

def folder_names(dates, parentdir) -> set:
    '''Creates Directories for distinct landings based on UTC Date column info --> Format = YYYY-MM-DD'''

    file_names = set()

    # Set of Folder names to be created
    for i in dates:
        if pd.isna(i) or i in file_names:
            continue
        file_names.add(i)
        
    # For every column make directory if it doesn't exist
    for i in file_names:
        # Partitions of Date values from UTC Date Column
        year = i[:4]
        month = i[5:7]
        day = i[8:10]

        # Can change month 12 to Dec if needed
        # calend = ['Jan', 'Feb', 'March', 'Apr', 'May', 'Jun','Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

        try:
            # If the directory doesnt exist for the yyyy/mm/dd make one
            if not os.path.exists(f'{parentdir}\{year}'):
                os.makedirs(f'{parentdir}\{year}')

            if not os.path.exists(f'{parentdir}\{year}\{month}'):
                os.makedirs(f'{parentdir}\{year}\{month}')
            
            if not os.path.exists(f'{parentdir}\{year}\{month}\{day}'):
                os.makedirs(f'{parentdir}\{year}\{month}\{day}')

        except Exception as ex:
            print(ex)

if __name__ == '__main__':
    main()