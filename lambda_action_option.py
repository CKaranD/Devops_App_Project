import os
from zusbot_main_no_tools import *
from json_object_maker import create_json_object
from detect_language import detect_language
from ada_options_checking import check_closer_option
from get_openai_key import openai_api_key
from template_main_v4 import (ZUS_LANGUAGE_INSTRUCTIONS, ZUS_PREFIX, ZUS_SUFFIX)

def lambda_action_option(mem_flag, pickled_memory_file, user_input, intent):
    # Set MPLCONFIGDIR to /tmp
    # os.environ['MPLCONFIGDIR'] = '/tmp'    
    
    llm = create_llm(openai_api_key)        

    if mem_flag == 0:
        memory = create_memory(llm)
        mem_flag += 1
    else:            
        memory = load_memory(pickled_memory_file)

    # detect input language
    language = detect_language(user_input)
    ZUS_TEMPLATE = ZUS_PREFIX + ZUS_LANGUAGE_INSTRUCTIONS + language + ZUS_SUFFIX        

    output, summary_value = zusbot(ZUS_TEMPLATE, llm, user_input, memory, pickled_memory_file)

    
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

    return output, summary_value, resolution_option
