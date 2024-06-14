def define_data_structure():
    SOWs = [
        'Commercial Intake Fax'
        ,'Promise Intake Fax'
        ,'Commercial Intake Phone'
        ,'Promise Intake Phone'
        ,'Intake Pharmacy'
        ,'UM RxMed'
        ,'Promise Pharmacy'
    ]
    available_data = {
        'Commercial Intake Fax':[['Image', 'Image Report']]
        ,'Promise Intake Fax':[['Image', 'Image Report']]
        ,'Commercial Intake Phone':[['DPL', 'Intake Phone']]
        ,'Promise Intake Phone':[['DPL', 'Intake Phone']]
        ,'Intake Pharmacy':[['Image', 'Image Report']]
        ,'UM RxMed':[['Image', 'Image Report']]
        ,'Promise Pharmacy':[['Image', 'Image Report']]
    }
    return SOWs, available_data