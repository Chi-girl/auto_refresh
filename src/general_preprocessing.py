import pandas as pd
import numpy as np
import datetime

def preprocess_master_df(master, ref_AHT):
    master['Month, Year'] = pd.to_datetime(master['Received Date/Time']).dt.strftime('%b-%Y')
    # master['Month #']
    master['File ID'] = ["Commercial {}".format(x+1) for x in range(master.shape[0])]
    master['Counter'] = 1

    master['Hour Bucket (Arrival)'] = master['Received Date/Time'].dt.hour.map("{:0>2}".format)
    master['Arrival Time'] = master['Received Date/Time'].dt.time
    master['Correct Hour Bucket (Arrival)'] = master.apply(bucket_hours, args=('Arrival',), axis=1)
    
    master['Hour Bucket (Processing)'] = master['Request Completed Datetime'].dt.hour.map("{:0>2}".format)
    master['Processing Time'] = master['Request Completed Datetime'].dt.time
    master['Correct Hour Bucket (Processing)'] = master.apply(bucket_hours, args=('Processing',), axis=1)
    
    master['Hour Type'] = np.where(
        (master['ReceivedTime']>=datetime.time(8,0,0)) & (master['ReceivedTime']<=datetime.time(17,0,0)), "Regular Hours", "Off Hours"
    )

    master['Target Contractual Hours'] = 6.5
    master['Hour Converter'] = 60
    master['CPT Code'] = np.nan

    master = master.merge(
        ref_AHT[['Service Line','Target AHT (mins)']], how='left', on='Service Line'
    )

    return master

def bucket_hours(line_item, type):
    if type=="Arrival": data_column = "Arrival Time"
    if type=="Processing": data_column = "Processing Time"
    
    if (line_item[data_column]>=datetime.time(0,0,0)) & (line_item[data_column]<datetime.time(1,0,0)): hour_range="12AM to 1AM"
    elif (line_item[data_column]>=datetime.time(1,0,0)) & (line_item[data_column]<datetime.time(2,0,0)): hour_range="1AM to 2AM"
    elif (line_item[data_column]>=datetime.time(2,0,0)) & (line_item[data_column]<datetime.time(3,0,0)): hour_range="2AM to 3AM"
    elif (line_item[data_column]>=datetime.time(3,0,0)) & (line_item[data_column]<datetime.time(4,0,0)): hour_range="3AM to 4AM"
    elif (line_item[data_column]>=datetime.time(4,0,0)) & (line_item[data_column]<datetime.time(5,0,0)): hour_range="4AM to 5AM"
    elif (line_item[data_column]>=datetime.time(5,0,0)) & (line_item[data_column]<datetime.time(6,0,0)): hour_range="5AM to 6AM"
    elif (line_item[data_column]>=datetime.time(6,0,0)) & (line_item[data_column]<datetime.time(7,0,0)): hour_range="6AM to 7AM"
    elif (line_item[data_column]>=datetime.time(7,0,0)) & (line_item[data_column]<datetime.time(8,0,0)): hour_range="7AM to 8AM"
    elif (line_item[data_column]>=datetime.time(8,0,0)) & (line_item[data_column]<datetime.time(9,0,0)): hour_range="8AM to 9AM"
    elif (line_item[data_column]>=datetime.time(9,0,0)) & (line_item[data_column]<datetime.time(10,0,0)): hour_range="9AM to 10AM"
    elif (line_item[data_column]>=datetime.time(10,0,0)) & (line_item[data_column]<datetime.time(11,0,0)): hour_range="10AM to 11AM"
    elif (line_item[data_column]>=datetime.time(11,0,0)) & (line_item[data_column]<datetime.time(12,0,0)): hour_range="11AM to 12PM"
    elif (line_item[data_column]>=datetime.time(12,0,0)) & (line_item[data_column]<datetime.time(13,0,0)): hour_range="12PM to 1PM"
    elif (line_item[data_column]>=datetime.time(13,0,0)) & (line_item[data_column]<datetime.time(14,0,0)): hour_range="1PM to 2PM"
    elif (line_item[data_column]>=datetime.time(14,0,0)) & (line_item[data_column]<datetime.time(15,0,0)): hour_range="2PM to 3PM"
    elif (line_item[data_column]>=datetime.time(15,0,0)) & (line_item[data_column]<datetime.time(16,0,0)): hour_range="3PM to 4PM"
    elif (line_item[data_column]>=datetime.time(16,0,0)) & (line_item[data_column]<datetime.time(17,0,0)): hour_range="4PM to 5PM"
    elif (line_item[data_column]>=datetime.time(17,0,0)) & (line_item[data_column]<datetime.time(18,0,0)): hour_range="5PM to 6PM"
    elif (line_item[data_column]>=datetime.time(18,0,0)) & (line_item[data_column]<datetime.time(19,0,0)): hour_range="6PM to 7PM"
    elif (line_item[data_column]>=datetime.time(19,0,0)) & (line_item[data_column]<datetime.time(20,0,0)): hour_range="7PM to 8PM"
    elif (line_item[data_column]>=datetime.time(20,0,0)) & (line_item[data_column]<datetime.time(21,0,0)): hour_range="8PM to 9PM"
    elif (line_item[data_column]>=datetime.time(21,0,0)) & (line_item[data_column]<datetime.time(22,0,0)): hour_range="9PM to 10PM"
    elif (line_item[data_column]>=datetime.time(22,0,0)) & (line_item[data_column]<datetime.time(23,0,0)): hour_range="10PM to 11PM"
    elif (line_item[data_column]>=datetime.time(23,0,0)) & (line_item[data_column]<=datetime.time(23,59,59)): hour_range="11PM to 12AM"
    else: hour_range = ""
    return hour_range