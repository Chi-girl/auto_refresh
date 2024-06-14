import helper_functions

def get_ref_files(data_dump):

    ref_TAT = helper_functions.read_file(data_path=data_dump+"\\References\\", data_file="image_lookups.xlsx", sheet_name='tat')
    ref_BD = helper_functions.read_file(data_path=data_dump+"\\References\\", data_file="image_lookups.xlsx", sheet_name='business_date')
    ref_AHT = helper_functions.read_file(data_path=data_dump+"\\References\\", data_file="image_lookups.xlsx", sheet_name='aht')

    return ref_TAT, ref_BD, ref_AHT