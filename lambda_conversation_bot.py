import os
import json
from zusbot_main_no_tools import *
from detect_language import detect_language
from get_openai_key import openai_api_key


def create_json_object(output, summary_value, mem_flag):
    data = {
        "output": output,
        "summary_value": summary_value,
        "mem_flag": mem_flag 
    }
    json_object = json.dumps(data)
    return json_object


def lambda_conversation_bot(event, context):
    # Set MPLCONFIGDIR to /tmp
    os.environ['MPLCONFIGDIR'] = '/tmp'

    mem_flag = event['mem_flag']
    pickled_memory_file = event['pickled_memory_file']
    user_input = event['user_input']
    intent = event['intent']
    status = event['status']

    llm = create_llm(openai_api_key)        

    if mem_flag == 0:
        memory = create_memory(llm)
        mem_flag = 1
    else:            
        memory = load_memory(pickled_memory_file)

    # detect input language
    language = detect_language(user_input)
            
    # conversation
    if intent == "slow delivery service":
        from template_sub_slow_delivery_service import (ZUS_LANGUAGE_INSTRUCTIONS, ZUS_PREFIX, ZUS_SUFFIX)
        ZUS_TEMPLATE = ZUS_PREFIX + ZUS_LANGUAGE_INSTRUCTIONS + language + ZUS_SUFFIX        
        # order_num = input("Bot reply: May I have your order number please? \n")
        # verify if the number is valid, and do some backend proces with order_num        
        # bot_flag = 1 # set bot_flag

    elif intent == "OOS":
        from template_sub_oos import (ZUS_LANGUAGE_INSTRUCTIONS, ZUS_PREFIX, ZUS_SUFFIX)
        ZUS_TEMPLATE = ZUS_PREFIX + ZUS_LANGUAGE_INSTRUCTIONS + language + ZUS_SUFFIX        
        # order_num = input("Bot reply: May I have your order number please? \n")
        # verify if the number is valid, and do some backend proces with order_num        
        # bot_flag = 2 # set bot_flag

    elif intent == "delivery info / status":
        from template_sub_delivery_info_status import (ZUS_LANGUAGE_INSTRUCTIONS, ZUS_PREFIX, ZUS_SUFFIX, SCHEME_SPLIT1, SCHEME_SPLIT2)        
        # order_num = input("Bot reply: May I have your order number please? \n")
        # check the status from the backend database and select the answering scheme (1) to (4)
        # for debug, we set the status here for testing
        # status = 3
        ZUS_TEMPLATE = ZUS_PREFIX + str(status) + SCHEME_SPLIT1 + str(status) + SCHEME_SPLIT2 + ZUS_LANGUAGE_INSTRUCTIONS + language + ZUS_SUFFIX        
    
    elif intent == "pickup info / status":
        from template_sub_pickup_info_status import (ZUS_LANGUAGE_INSTRUCTIONS, ZUS_PREFIX, ZUS_SUFFIX, SCHEME_SPLIT1, SCHEME_SPLIT2)        
        # order_num = input("Bot reply: May I have your order number please? \n")
        # check the status from the backend database and select the answering scheme (1) to (4)
        # for debug, we set the status here for testing
        # status = 3
        ZUS_TEMPLATE = ZUS_PREFIX + str(status) + SCHEME_SPLIT1 + str(status) + SCHEME_SPLIT2 + ZUS_LANGUAGE_INSTRUCTIONS + language + ZUS_SUFFIX        
        
    elif intent == "zus career":
        from template_sub_career import (ZUS_LANGUAGE_INSTRUCTIONS, ZUS_PREFIX, ZUS_SUFFIX)
        ZUS_TEMPLATE = ZUS_PREFIX + ZUS_LANGUAGE_INSTRUCTIONS + language + ZUS_SUFFIX

    # add more of such rule here for other intents
    
    else:
        from template_main_v4 import (ZUS_LANGUAGE_INSTRUCTIONS, ZUS_PREFIX, ZUS_SUFFIX)
        ZUS_TEMPLATE = ZUS_PREFIX + ZUS_LANGUAGE_INSTRUCTIONS + language + ZUS_SUFFIX        
    
    output, summary_value = zusbot(ZUS_TEMPLATE, llm, user_input, memory, pickled_memory_file)

    json_obj = create_json_object(output, summary_value, mem_flag)
    
    return json_obj


