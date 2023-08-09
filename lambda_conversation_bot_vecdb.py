import os
import json
from zusbot_main_no_tools import *
from detect_language import detect_language
from get_openai_key import openai_api_key
from query_chromadb import get_qa_chain
from template_main_v4 import (ZUS_LANGUAGE_INSTRUCTIONS, ZUS_PREFIX, ZUS_SUFFIX)


def create_json_object(output, summary_value, mem_flag, vecdb_flag, eot_flag):
    data = {
        "output": output,
        "summary_value": summary_value,
        "mem_flag": mem_flag,
        "vecdb_flag": vecdb_flag,
        "eot_flag": eot_flag  
    }
    json_object = json.dumps(data)
    return json_object


def lambda_conversation_bot_vecdb(event, context):
    # Set MPLCONFIGDIR to /tmp
    os.environ['MPLCONFIGDIR'] = '/tmp'

    mem_flag = event['mem_flag']
    pickled_memory_file = event['pickled_memory_file']
    user_input = event['user_input']
    intent = event['intent']

    llm = create_llm(openai_api_key)        

    if mem_flag == 0:
        memory = create_memory(llm)
        mem_flag = 1
    else:            
        memory = load_memory(pickled_memory_file)

    # detect input language and set template
    language = detect_language(user_input)
    ZUS_TEMPLATE = ZUS_PREFIX + ZUS_LANGUAGE_INSTRUCTIONS + language + ZUS_SUFFIX        
            
    # DB retrieval directories
    if intent == "loyalty benefits":
        db_path = 'db/loyalty_benefits'
    
    elif intent == "product / menu details":
        db_path = 'db/products_menu'

    # add more of such rule here for other intents
    
    qa_chain = get_qa_chain(db_path)
    output = qa_chain.run(user_input)
    _, summary_value = zusbot_vectordb(ZUS_TEMPLATE, intent, output, llm, user_input, memory, pickled_memory_file)

    vecdb_flag = 1
    eot_flag = 0 # always return eot_flag = 0

    json_obj = create_json_object(output, summary_value, mem_flag, vecdb_flag, eot_flag)
    
    return json_obj


