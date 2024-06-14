# import libraries
import pandas as pd
import numpy as np
from os import listdir
from os.path import isfile, join
import warnings
warnings.filterwarnings('ignore')

# get names of the data files
def get_filenames(data_path):
    data_files = [f for f in listdir(data_path) if isfile(join(data_path, f))]
    return data_files

def read_file(data_path, data_file, sheet_name=0, skiprows=0):
    df = pd.read_excel(data_path + data_file, sheet_name=sheet_name, skiprows=skiprows)

    return df

def get_subfolder_name(SOW, report_type):
    subfolder_name = SOW
    if SOW in ['Intake Pharmacy','UM RxMed','Promise Pharmacy']:
        if report_type == 'Image':
            subfolder_name = "Intake Pharmacy, UM RxMed, Promise Pharmacy"
    return subfolder_name

def rename_headers(df):
    columns_to_be_renamed = {
        "Baseline Payment Dte": "Baseline Date"
        ,"SOURCE": "Source/Doc Type"
    }
    columns = df.columns
    for column in columns:
        if column in columns_to_be_renamed.keys():
            df.rename(columns={column:columns_to_be_renamed[column]}, inplace=True)
    return df