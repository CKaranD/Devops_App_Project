import os
import json
from ada_options_checking import check_closer_option


def create_json_object(resolution_option, option_flag, option_done_flag):
    data = {
        "resolution_option": resolution_option,
        "option_flag": option_flag,
        "option_done_flag": option_done_flag   
    }
    json_object = json.dumps(data)
    return json_object


def lambda_action_option(event, context):
    # Set MPLCONFIGDIR to /tmp
    os.environ['MPLCONFIGDIR'] = '/tmp'

    user_input = event['user_input']
    intent = event['intent']
    
    resolution_option = "None"
    
    # slow delivery service
    if intent == "slow delivery service":
        options = [
            "option (1): Cancel the order with a refund",
            "option (2): Take the 'ZUSSORRY' voucher"
        ]
        resolution_option = check_closer_option(user_input, options)
    
    # OOS
    elif intent == "OOS":
        options = [
            "option (1): Cancel the order with full refund",
            "option (2): Take partial refund"
        ]
        resolution_option = check_closer_option(user_input, options)

    option_flag = 0
    option_done_flag = 1

    json_obj = create_json_object(resolution_option, option_flag, option_done_flag)

    return json_obj
