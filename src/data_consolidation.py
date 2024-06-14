# import libraries
from email.mime import image
import pandas as pd
import numpy as np
from datetime import datetime
import helper_functions
import warnings
warnings.filterwarnings('ignore')

# Image Data

def consolidate_image_data(SOW, data_files_loc, data_files, sheet_name, ref_BD, ref_TAT):
    print(SOW)
    # initialize frame
    image = pd.DataFrame()

    # read data dumped
    for data_file in data_files:
        df = helper_functions.read_file(data_files_loc, data_file, sheet_name=sheet_name)
        image = image.append(df)
    
    # filter data accordingly
    if SOW == 'Intake Pharmacy':
        image = image[image['Routing']=='Pharmacy Intake']
    elif SOW == 'UM RxMed':
        image = image[image['Routing']=='UM IN- Medication Request']
    elif SOW == 'Promise Pharmacy':
        image = image[image['Routing']=='Promise RX Intake']

    # add additional columns
    image = compute_additional_columns(image, SOW, ref_BD, ref_TAT)
    
    # remove case duplicates
    #image.drop_duplicates(subset=['File Name'], keep='last', inplace=True)    
    
    return image

def add_basic_details(df, SOW):
    df['Location'] = "Manila"
    df['File_Name'] = df['File Name'].str.strip()
    df['File_Name'] = df['File_Name'].fillna("N/A")

    if (SOW == 'Intake Pharmacy') | (SOW == 'UM RxMed') | (SOW == 'Promise Pharmacy'):
        df['File_Name_Count'] = df.apply(count_filename, args=(df['File_Name'],), axis=1)
        df['File_Name_Count'] = pd.to_numeric(df['File_Name_Count'], errors="coerce")
        df['File_Name_Unique'] = np.where(df['File_Name_Count']==1, 1, 0)
    return df

def add_routing_queue(df, SOW):
    df['File_Name_Component'] = [filename[:3] for filename in df['File_Name']]
    df['Routing Queue'] = np.where(
        df['Routing']=="UM IN- Medicare 65+ Request", np.where(
            df['File_Name_Component'].isin(['UMB','UMC','UMD','UMU','UMV','UMW','THO']), 'UM IN- Medicare 65+ INP Request', 'UM IN- Medicare 65+ Prior Auth Request'
        ),
        df['Routing']
    )

    if (SOW == 'Intake Pharmacy') | (SOW == 'UM RxMed') | (SOW == 'Promise Pharmacy'):
        df['SOW'] = SOW
    return df

def add_received_date_details(df, SOW):
    if (SOW == 'Intake Pharmacy') | (SOW == 'UM RxMed') | (SOW == 'Promise Pharmacy'):
        df['Received Date_Orig'] = np.where(df['Received Date/Time'].isnull(), np.nan, pd.to_datetime(df['Received Date/Time']).dt.date)
    df['Received Date_Orig'] = pd.to_datetime(df['Received Date_Orig'])
    df['ReceivedTime'] = pd.to_datetime(df['Received Date/Time']).dt.time
    df['ReceivedTime_day'] = (pd.to_datetime(df['Received Date/Time']).dt.hour + pd.to_datetime(df['Received Date/Time']).dt.minute / 60) / 24
    df['Day_Recd Orig'] = [day_name[:3] for day_name in df['Received Date_Orig'].dt.day_name()]
    return df

def merge_with_reftable_TAT(df, SOW, ref_TAT):
    if (SOW=="Commercial Intake Phone") | (SOW=="Promise Intake Phone"):
        df['TAT1'] = 24
    else:
        df = df.merge(
            ref_TAT[['Routing Queue', 'TAT1', 'TAT2', 'TAT3', 'TAT4']], how='left', on='Routing Queue'
        )
    return df

def merge_with_reftable_BD(df, SOW, ref_BD, left_df_key):
    df = df.merge(
        ref_BD[['DATE', 'BD + Non WORKDAY', 'BD']], how='left', left_on=left_df_key, right_on='DATE'
    )
    return df

def drop_extra_columns(df):
    df.drop(['DATE', 'BD + Non WORKDAY', 'BD'], axis=1, inplace=True)

def add_receiveddt_adjustments(df, SOW):
    if (SOW == 'Intake Pharmacy') | (SOW == 'UM RxMed') | (SOW == 'Promise Pharmacy'):
        df['Received Date_New'] = np.where(
            (df['BD']==0) | (df['ReceivedTime_day'] > df['TAT2']),
            df['Received Date_Orig'] + df['BD + Non WORKDAY'].apply(lambda x: pd.Timedelta(x, unit='D')),
            df['Received Date_Orig']
        )
    df['Day_Recd New'] = [day_name[:3] for day_name in pd.to_datetime(df['Received Date_New']).dt.day_name()]
    df['Month_Received_New'] = pd.to_datetime(df['Received Date_New']).dt.strftime('%b-%Y')
    return df

def add_completion_date(df):
    df['Completed Date'] = np.where(
        df['Request Completed Datetime'].isnull(), np.nan,
        pd.to_datetime(df['Request Completed Datetime']).dt.date
    )
    df['Month_Completed'] = pd.to_datetime(df['Completed Date']).dt.strftime('%b-%Y')
    return df

def add_validation(df, SOW):
    df['RecdDate Validation'] = np.where(df['Received Date_Orig']==df['Received Date_New'], "TRUE", "FALSE")
    df['ReceivedDateTime_New'] = np.where(df['RecdDate Validation']=="TRUE",df['Received Date/Time'],df['Received Date_New'])
    ## BD based on Received Date_New
    if (SOW == 'Intake Pharmacy') | (SOW == 'UM RxMed') | (SOW == 'Promise Pharmacy'):
        df['Validation'] = np.where(
            df['Received Date/Time']==df['ReceivedDateTime_New'],
            df['ReceivedDateTime_New'] + df['BD + Non WORKDAY'].apply(lambda x: pd.Timedelta(x, unit='D')) + pd.to_timedelta(df['TAT3']),
            df['ReceivedDateTime_New'] + df['BD + Non WORKDAY'].apply(lambda x: pd.Timedelta(x, unit='D')) + pd.to_timedelta(df['TAT4'])
        )

    df['Validation_Date'] = pd.to_datetime(df['Validation']).dt.date
    return df

def add_actual_vs_expected_completion(df, SOW):
    df['CompletedDateTime_Actual'] = pd.to_datetime(df['Request Completed Datetime'])
    ## BD based on Validation_Date
    if (SOW == 'Intake Pharmacy') | (SOW == 'UM RxMed') | (SOW == 'Promise Pharmacy'):
        df['CompletedDateTime_Expected'] = np.where(
            df['BD']==1, df['Validation'], df['Validation'] + df['BD + Non WORKDAY'].apply(lambda x: pd.Timedelta(x, unit='D'))
        )
    else:
        df['CompletedDateTime_Expected'] = df['Received Date/Time'] + df['TAT1'].apply(lambda x: pd.Timedelta(x, unit='H'))
    return df

def add_tat_computation(df, SOW):
    if (SOW == 'Intake Pharmacy') | (SOW == 'UM RxMed') | (SOW == 'Promise Pharmacy'):
        df['TotalTime_ClaimToCom'] = (pd.to_timedelta(df['Request Completed Datetime'] - df['Claim Datetime']).dt.components['days'] * 24) + \
            (pd.to_timedelta(df['Request Completed Datetime'] - df['Claim Datetime']).dt.components['hours']) + \
            (pd.to_timedelta(df['Request Completed Datetime'] - df['Claim Datetime']).dt.components['minutes'] / 60)

        df['Completion_Actual_vs_Expected']= (pd.to_timedelta(df['CompletedDateTime_Actual'] - df['CompletedDateTime_Expected']).dt.components['days'] * 24) + \
                                            (pd.to_timedelta(df['CompletedDateTime_Actual'] - df['CompletedDateTime_Expected']).dt.components['hours']) + \
                                            (pd.to_timedelta(df['CompletedDateTime_Actual'] - df['CompletedDateTime_Expected']).dt.components['minutes'] / 60)
                                            
        df['TotalTime_RecToCom'] = np.where(df['CompletedDateTime_Actual'] <= df['CompletedDateTime_Expected'], 0, df['TAT1'] + df['Completion_Actual_vs_Expected'])
    return df

def add_pass_or_fail_tagging(df):
    df['TAT_RecdToCom'] = np.where(df['TotalTime_RecToCom'] > df['TAT1'], "FAIL", "PASS")
    df['TAT_ClaimToCom'] = np.where(df['TotalTime_RecToCom'] > df['TAT1'], "FAIL", "PASS")
    df['Pass'] = np.where(df['TAT_RecdToCom']=="PASS", 1, 0)
    df['Fail'] = np.where(df['TAT_RecdToCom']=="FAIL", 1, 0)
    df['Pass_Claim'] = np.where(df['TAT_ClaimToCom']=="PASS", 1, 0)
    df['Fail_Claim'] = np.where(df['TAT_ClaimToCom']=="FAIL", 1, 0)
    return df

def compute_additional_columns(df, SOW, ref_BD, ref_TAT):
    df['Service Line'] = SOW
    print(df.shape)
    if (SOW == 'Intake Pharmacy') | (SOW == 'UM RxMed') | (SOW == 'Promise Pharmacy') | (SOW=="Commercial Intake Phone") | (SOW=="Promise Intake Phone"):
        df = add_basic_details(df, SOW)
        df = add_routing_queue(df, SOW)
        df = add_received_date_details(df, SOW)

        df = merge_with_reftable_TAT(df, SOW, ref_TAT)
        df = merge_with_reftable_BD(df, SOW, ref_BD, left_df_key="Received Date_Orig")

        df = add_receiveddt_adjustments(df, SOW)
        df = add_completion_date(df)
        df = add_validation(df, SOW)
        df = add_actual_vs_expected_completion(df, SOW)
        df = add_tat_computation(df, SOW)
        df = add_pass_or_fail_tagging(df)
    return df


def count_filename(line_item, filenames):
    filename_count = filenames.isin([line_item['File_Name']]).sum()
    return filename_count

# DPL data
def consolidate_dpl_data(SOW, data_files_loc, data_files, sheet_name, skiprows, ref_BD, ref_TAT):
    print(SOW)
    dpl = pd.DataFrame()
    for data_file in data_files:
        df = helper_functions.read_file(data_files_loc, data_file, sheet_name=sheet_name, skiprows=skiprows)
        dpl = dpl.append(df)

    if (SOW == "Commercial Intake Phone") | (SOW == "Promise Intake Phone"):
        dpl = preprocess_intake_phone(dpl)
        dpl = compute_additional_columns(dpl, SOW, ref_BD, ref_TAT)
    
    return dpl

def preprocess_intake_phone(dpl):
    dpl['Multiple Count'] = dpl['Multiple Count'].fillna(0)
    dpl['Multiple Count'] = pd.to_numeric(dpl['Multiple Count'].astype(str).str.replace(',',''), errors='coerce').fillna(0).astype(int)
    dpl['Multiple'] = np.where(dpl['Multiple']=="Yes", 0, 1)

    dpl.rename(columns={
        "TimeStamp":"Received Date/Time"
        ,"Name":"User ID"
        ,"Call Type":"Request Type"
        ,"Reference ID":"File Name"
        ,"BSC Prod Date":"Received Date_Orig"
        ,"Multiple":"File_Name_Unique"
        ,"Multiple Count":"File_Name_Count"
        ,"Team":"SOW"
        ,"Sub Call Type":"Routing"
    }, inplace=True)

    dpl['Claim Datetime'] = dpl["Received Date/Time"]
    dpl['Received Date_New'] = dpl['Received Date_Orig']
    dpl['Request Completed Datetime'] = pd.to_datetime(dpl['Received Date/Time']) + dpl['Processing Time'].apply(lambda x: pd.Timedelta(x, unit='S'))
    dpl['TotalTime_RecToCom'] = dpl['Processing Time'] / 60 / 60
    dpl['TotalTime_ClaimToCom'] = dpl['TotalTime_RecToCom']
    dpl['Validation'] = dpl["Received Date/Time"]
    dpl['TAT1'] = 24
    
    return dpl

# def consolidate_pa_inventory(data_files_loc, data_files):
#     pa_inventory = pd.DataFrame()
#     for data_file in data_files:
#         df = helper_functions.read_file(data_files_loc, data_file)
#         pa_inventory = pa_inventory.append(df)
    
#     return pa_inventory

# def consolidate_commercial_call_back(data_files_loc, data_files):
#     commercial_call_back = pd.DataFrame()
#     for data_file in data_files:
#         df = helper_functions.read_file(data_files_loc, data_file)
#         commercial_call_back = commercial_call_back.append(df)
    
#     return commercial_call_back