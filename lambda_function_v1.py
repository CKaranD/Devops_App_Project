# we will only attend to this function when all dev is done

import os
from zusbot_main_no_tools import *
from json_object_maker import create_json_object
from detect_language import detect_language

def lambda_handler(event, context):
    # Set MPLCONFIGDIR to /tmp
    os.environ['MPLCONFIGDIR'] = '/tmp'
    
    mem_flag = event['mem_flag']    
    pickled_memory_file = event['pickled_memory_file']
    user_input = event['user_input']

    openai_api_key = keygen()

    llm = create_llm(openai_api_key)        

    if mem_flag == 0:
        memory = create_memory(llm)
        mem_flag += 1
    else:            
        memory = load_memory(pickled_memory_file)

    # detect input language
    language = detect_language(user_input)
    
    output, summary_value = zusbot(language, llm, user_input, memory, pickled_memory_file)

    json_obj = create_json_object(user_input, output, summary_value, mem_flag)

    return json_obj