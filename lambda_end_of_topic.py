import os
from end_of_topic_detector import EOT_checker

def lambda_end_of_topic(customer_input, eot_flag, vecdb_flag):
    # Set MPLCONFIGDIR to /tmp
    # os.environ['MPLCONFIGDIR'] = '/tmp'    
    
    eot_yes_no = EOT_checker(customer_input)
    if eot_yes_no == "yes":
        eot_flag = 1            
        vecdb_flag = 0        
    else:
        eot_flag = eot_flag            
        vecdb_flag = vecdb_flag
        
    return eot_flag, vecdb_flag
