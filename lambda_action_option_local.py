import os
from json_object_maker import create_json_object
from ada_options_checking import check_closer_option


def lambda_action_option(user_input, intent):
    # Set MPLCONFIGDIR to /tmp
    # os.environ['MPLCONFIGDIR'] = '/tmp'    
        
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

    return resolution_option, option_flag, option_done_flag
