import winsound
import time
import os
import sys
import glob
import pandas as pd
import datetime 
import locale

"""
Insert paths namely sources and outputs folders
    ex. 
        data_source_1  = "Worklist"
        data_source_2 = "Agent"
    Output:
        output_source = ".dashboard"
    Lookups:
        can be redirected to file name itself
        lookup_forex = "lookup\exchange_rate.csv"
"""
#************************************************
# MAIN PATHS                                    
data_source1 = "Datasource\source 1"
output_source = "Datasource\.dashboard"
#************************************************
def read_csv(data_source, df):
    
    return df


def main():
# THIS IS JUST FOR TESTING TO ADD AUDIO CLUE WHEN RUNNING OR TESTING
    frequency = 2500  # Frequency in Hertz
    duration = 2000  # Duration in milliseconds
    winsound.Beep(frequency, duration)
    time.sleep(1)
#get local pc location ------------------------------------------------------------------------------------------------------------
    # def get_country():
    #     # Get the default locale
    #     default_locale = locale.getdefaultlocale()

    #     # Extract the country from the default locale
    #     country = default_locale[0].split('_')[-1]

    #     return country
# -----------------------------------------------------------------------------------------------------------------------------------

#DATASOURCE 1

# Get the directory path containing the executable -- so we wont be needing to declaire or input the source per user
    executable_path = os.path.abspath(sys.argv[0])
    executable_directory = os.path.dirname(executable_path)
    print("\Path check = ",executable_directory) # check if will return correct path

    # Change the current working directory to 'Datasource' folder inside the directory of the executable
    os.chdir(os.path.join(executable_directory, data_source1))

    # Read the existing OUTPUT.csv file if it exists
    existing_output_path = os.path.join(executable_directory, output_source, "output1.parquet.gzip")
    if os.path.exists(existing_output_path):
        df_con = pd.read_parquet(existing_output_path)
    else:
        df_con = pd.DataFrame()

    # Read the list of already loaded files from Record.txt
    record_file_path = os.path.join(executable_directory,output_source, "Record.txt")
    loaded_files = []  # List to store filenames of loaded files in order
    if os.path.exists(record_file_path):
        with open(record_file_path, "r") as record_file:
            for line in record_file:
                filename = line.strip()
                if filename:
                    loaded_files.append(filename)

    files = glob.glob("*.xlsb") 

    for file in files:
        # Check if the file has already been loaded
        if file in loaded_files:
            print(f"Skipping file '{file}' as it has already been loaded.")   # Shows what file is currently loaded
            continue
        try: 
            """
            add parameter if needed
                ex. sheet_name = "Sheet1"
                    engine = "pyxlsb"

            """
            df = pd.read_excel(file)    
        except:
            df = pd.read_excel(file, engine='pyxlsb')

        print('\n', file, df.shape)
        df['file'] = file    # record file name
        df["file_timestamp"] = datetime.datetime.now() # record time and date when the file was loaded
        # df["country"] = get_country() # get local pc country
        df_con = pd.concat([df_con,df])
        
        # Append the filename to the list of loaded files
        loaded_files.append(file)

    # Save the concatenated DataFrame to a CSV file in the 'test' folder
    df_con = df_con.astype(str)
    df_con.to_parquet(existing_output_path, compression='gzip',index=False)
    
    print("Output saved to:", existing_output_path)

    # Write the updated list of loaded files to Record.txt maintaining the order
    with open(record_file_path, "w") as record_file:
        for loaded_file in loaded_files:
            record_file.write(loaded_file + "\n")
#Record application trigger
        record_file.write("EXECUTABLE trigger stamp = ")
        current_datetime = datetime.datetime.now()
        current_datetime_str = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        record_file.write(current_datetime_str + "\n"+ "\n")

if __name__ == "__main__":
    main()
