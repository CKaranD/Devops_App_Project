import os
from zusbot_main_no_tools import *
from json_object_maker import create_json_object
from detect_language import detect_language
from get_openai_key import openai_api_key
from query_chromadb import get_qa_chain
from template_main_v4 import (ZUS_LANGUAGE_INSTRUCTIONS, ZUS_PREFIX, ZUS_SUFFIX)


def lambda_conversation_bot_vecdb(mem_flag, pickled_memory_file, user_input, intent):
    # Set MPLCONFIGDIR to /tmp
    # os.environ['MPLCONFIGDIR'] = '/tmp'    
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

    elif intent == "birthday / vouchers":
        db_path = 'db/birthday_vouchers'

    # add more of such rule here for other intents
    
    qa_chain = get_qa_chain(db_path)
    output = qa_chain.run(user_input)
    _, summary_value = zusbot_vectordb(ZUS_TEMPLATE, intent, output, llm, user_input, memory, pickled_memory_file)

    vecdb_flag = 1
    eot_flag = 0 # always return eot_flag = 0

    return output, summary_value, mem_flag, vecdb_flag, eot_flag

    # json_obj = create_json_object(user_input, output, summary_value, mem_flag)
    
    # return output, summary_value, mem_flag, bot_flag, option_flag, resolution_option


