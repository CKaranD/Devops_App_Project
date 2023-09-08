import os
import json
from chat_memory_manager import memory_manager
from zus_write_load_mem import load_memory
from system_messenger import response_system_msg


def create_json_object(translated_sys_msg, summary_value):
    data = {
        "translated_sys_msg": translated_sys_msg,
        "summary_value": summary_value
    }
    json_object = json.dumps(data)
    return json_object


def lambda_system_msg(event, context):
    # Set MPLCONFIGDIR to /tmp
    os.environ['MPLCONFIGDIR'] = '/tmp'  

    pickled_memory_file = event['pickled_memory_file']
    user_input = event['user_input']
    sys_msg = event['sys_msg']

    memory = load_memory(pickled_memory_file)    
    summary_value = memory_manager(memory, pickled_memory_file, user_input, sys_msg)
    translated_sys_msg = response_system_msg(user_input, sys_msg)
    
    json_obj = create_json_object(translated_sys_msg, summary_value)
    
    return json_obj


# debug lines
# pickled_memory_file = "my_local_test.pickle"
# sys_msg = "Please enter your order number of the transaction in the correct format. (eg: AB1122334455)"
# summary_value = lambda_chat_memory_manager(pickled_memory_file, sys_msg)
# print(summary_value)