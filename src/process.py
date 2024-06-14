from hashlib import algorithms_available
import pandas as pd
import helper_functions
import data_structure
import ref_files_access
from required_columns import define_required_columns
import data_consolidation
import general_preprocessing

import logging

logging.basicConfig(filename="assets/debug.log",
                    format="%(asctime)s - %(message)s",
                    level=logging.INFO,
                    datefmt="%Y-%m-%d %I:%M:%S%p")

def analyze(data_dump_path, progress):
    #try:        
    # define refresh parameters and data structure
    data_dump = data_dump_path
    output_path = data_dump_path + "\\_PREPROCESSED\\"
    SOWs, available_data = data_structure.define_data_structure()

    # data consolidation
    master = pd.DataFrame()
    for SOW in SOWs:
        progress("Reading {} data files...".format(SOW.upper()), 10)
        
        # list available data per SOW
        data_sets = available_data[SOW]

        # read reference files for image data
        ref_TAT, ref_BD, ref_AHT = ref_files_access.get_ref_files(data_dump)

        for data_set in data_sets:
            report_type = data_set[0]
            sheet_name = data_set[1]

            subfolder_name = helper_functions.get_subfolder_name(SOW, report_type)
            data_files_loc = data_dump + "\\" + report_type + "\\" + subfolder_name + "\\"
            data_files = helper_functions.get_filenames(data_files_loc)

            # consolidate data per data set type
            if report_type == 'Image':
                image = data_consolidation.consolidate_image_data(SOW, data_files_loc, data_files, sheet_name, ref_BD, ref_TAT)
            if report_type == 'DPL':
                dpl = data_consolidation.consolidate_dpl_data(SOW, data_files_loc, data_files, sheet_name, skiprows=5, ref_BD=ref_BD, ref_TAT=ref_TAT)

        if (SOW == 'Commercial Intake Fax') | (SOW == 'Promise Intake Fax') | (SOW == 'Intake Pharmacy') | (SOW == 'UM RxMed') | (SOW == 'Promise Pharmacy'):
            master_sow = image
        elif (SOW=="Commercial Intake Phone") | (SOW=="Promise Intake Phone"):
            master_sow = dpl
        
        # append dataframe per SOW to the master frame
        master = master.append(master_sow)

    # apply general preprocessing
    progress("Adding derived columns...", 10)
    master = general_preprocessing.preprocess_master_df(master, ref_AHT)

    # save output
    progress("Saving the preprocessed data...", 10)
    required_columns = define_required_columns()
    master[required_columns].to_excel(output_path + "Staffing_Optimization.xlsx", index=False)
    
    progress("Data preprocessing done!", 10)
    return "success"
        
    # except Exception as e:
    #     logging.exception("Exception occurred")
    #     return "Exception occurred"
        