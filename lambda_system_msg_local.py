import os
from chat_memory_manager import memory_manager
from json_object_maker import create_json_object
from zus_write_load_mem import load_memory
from system_messenger import response_system_msg


def lambda_system_msg(pickled_memory_file, user_input, sys_msg):
    # Set MPLCONFIGDIR to /tmp
    # os.environ['MPLCONFIGDIR'] = '/tmp'    
    memory = load_memory(pickled_memory_file)    
    summary_value = memory_manager(memory, pickled_memory_file, user_input, sys_msg)
    translated_sys_msg = response_system_msg(user_input, sys_msg)
    
    return translated_sys_msg, summary_value

    # json_obj = create_json_object(user_input, output, summary_value, mem_flag)
    
    # return output, summary_value, mem_flag, bot_flag, option_flag, resolution_option


# debug lines
# pickled_memory_file = "my_local_test.pickle"
# sys_msg = "Please enter your order number of the transaction in the correct format. (eg: AB1122334455)"
# summary_value = lambda_chat_memory_manager(pickled_memory_file, sys_msg)
# print(summary_value)