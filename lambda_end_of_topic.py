import os
import json
from end_of_topic_detector import EOT_checker


def create_json_object(eot_flag, vecdb_flag):
    data = {
        "eot_flag": eot_flag,
        "vecdb_flag": vecdb_flag  
    }
    json_object = json.dumps(data)
    return json_object


def lambda_end_of_topic(event, context):
    # Set MPLCONFIGDIR to /tmp
    os.environ['MPLCONFIGDIR'] = '/tmp'

    user_input = event['user_input']
    eot_flag = event['eot_flag']
    vecdb_flag = event['vecdb_flag']
    
    eot_yes_no = EOT_checker(user_input)
    if eot_yes_no == "yes":
        eot_flag = 1            
        vecdb_flag = 0        
    else:
        eot_flag = eot_flag            
        vecdb_flag = vecdb_flag
        
    json_obj = create_json_object(eot_flag, vecdb_flag)
    return json_obj
