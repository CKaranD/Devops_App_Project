import os
from zusbot_main_no_tools import *
from json_object_maker import create_json_object
from detect_language import detect_language
from mlp_classifier import mlp_classifier
from pre_negative_intent_classifier import pre_level_classifier
from translation import translator
from ada_options_checking import check_closer_option
from get_openai_key import openai_api_key
from query_chromadb import get_qa_chain


def lambda_handler(mem_flag, bot_flag, option_flag, pickled_memory_file, user_input):
    # Set MPLCONFIGDIR to /tmp
    # os.environ['MPLCONFIGDIR'] = '/tmp'    
    # openai_api_key = keygen()

    llm = create_llm(openai_api_key)        

    if mem_flag == 0:
        memory = create_memory(llm)
        mem_flag += 1
    else:            
        memory = load_memory(pickled_memory_file)

    # detect input language
    language = detect_language(user_input)
    
    # classify intent
    trans_user_input = user_input
    pre_intent = pre_level_classifier(trans_user_input)
    if pre_intent == "negative intent":
        pred = pre_intent
    else:        
        if language != "English":
            trans_user_input = translator(trans_user_input)
            trans_user_input = trans_user_input.replace("\n", " ")

        mlp_intent, confidence = mlp_classifier(trans_user_input)
        
        if confidence <= 0.18:
            pred = "negative intent"
        else:
            if mlp_intent == "hr partnership" and confidence <= 0.6:
                pred = "negative intent"
            else:                
                pred = mlp_intent
    print("Intent detected: ", pred)
    
    # conversation
    is_vectordb = False
    db_path = None
    if pred == "slow delivery service":
        from template_sub_slow_delivery_service import (ZUS_LANGUAGE_INSTRUCTIONS, ZUS_PREFIX, ZUS_SUFFIX)
        ZUS_TEMPLATE = ZUS_PREFIX + ZUS_LANGUAGE_INSTRUCTIONS + language + ZUS_SUFFIX        
        order_num = input("Bot reply: May I have your order number please? \n")
        # verify if the number is valid, and do some backend proces with order_num        
        bot_flag = 1 # set bot_flag

    elif pred == "OOS":
        from template_sub_oos import (ZUS_LANGUAGE_INSTRUCTIONS, ZUS_PREFIX, ZUS_SUFFIX)
        ZUS_TEMPLATE = ZUS_PREFIX + ZUS_LANGUAGE_INSTRUCTIONS + language + ZUS_SUFFIX        
        order_num = input("Bot reply: May I have your order number please? \n")
        # verify if the number is valid, and do some backend proces with order_num        
        bot_flag = 2 # set bot_flag

    elif pred == "delivery info / status":
        from template_sub_delivery_info_status import (ZUS_LANGUAGE_INSTRUCTIONS, ZUS_PREFIX, ZUS_SUFFIX, SCHEME_SPLIT1, SCHEME_SPLIT2)        
        order_num = input("Bot reply: May I have your order number please? \n")
        # check the status from the backend database and select the answering scheme (1) to (4)
        # for debug, we set the status here for testing
        status = 3
        ZUS_TEMPLATE = ZUS_PREFIX + str(status) + SCHEME_SPLIT1 + str(status) + SCHEME_SPLIT2 + ZUS_LANGUAGE_INSTRUCTIONS + language + ZUS_SUFFIX        
        
    elif pred == "zus career":
        from template_sub_career import (ZUS_LANGUAGE_INSTRUCTIONS, ZUS_PREFIX, ZUS_SUFFIX)
        ZUS_TEMPLATE = ZUS_PREFIX + ZUS_LANGUAGE_INSTRUCTIONS + language + ZUS_SUFFIX

    elif pred == "loyalty benefits":
        from template_main_v4 import (ZUS_LANGUAGE_INSTRUCTIONS, ZUS_PREFIX, ZUS_SUFFIX)
        ZUS_TEMPLATE = ZUS_PREFIX + ZUS_LANGUAGE_INSTRUCTIONS + language + ZUS_SUFFIX
        is_vectordb = True
        db_path = 'db/loyalty_benefits'

    # add more of such rule here for other intents, 
    # may need to re-organize their sequence and bot_flag for better visual
    else:
        from template_main_v4 import (ZUS_LANGUAGE_INSTRUCTIONS, ZUS_PREFIX, ZUS_SUFFIX)
        ZUS_TEMPLATE = ZUS_PREFIX + ZUS_LANGUAGE_INSTRUCTIONS + language + ZUS_SUFFIX        
    
    if is_vectordb == False:
        output, summary_value = zusbot(ZUS_TEMPLATE, llm, user_input, memory, pickled_memory_file)
    else:
        qa_chain = get_qa_chain(db_path)
        output = qa_chain.run(user_input)
        _, summary_value = zusbot_vectordb(ZUS_TEMPLATE, pred, output, llm, user_input, memory, pickled_memory_file)

    # check bot_flag, and get user's response
    if bot_flag == 0:
        resolution_option = "None"
    
    # slow delivery service
    elif bot_flag == 1:
        resolution_option = "None"
        option_flag += 1
        if option_flag >= 2:
            options = [
                "option (1): Cancel the order with a refund",
                "option (2): Take the 'ZUSSORRY' voucher"
            ]
            resolution_option = check_closer_option(user_input, options)
            option_flag = 0
            bot_flag = 0
    
    # OOS
    elif bot_flag == 2:
        resolution_option = "None"
        option_flag += 1
        if option_flag >= 2:
            options = [
                "option (1): Cancel the order with full refund",
                "option (2): Take partial refund"
            ]
            resolution_option = check_closer_option(user_input, options)
            option_flag = 0
            bot_flag = 0

    # json_obj = create_json_object(user_input, output, summary_value, mem_flag)
    
    return output, summary_value, mem_flag, bot_flag, option_flag, resolution_option



# ============= local test starts here 
# ============= (simulation of middleware)
mem_flag = 0
bot_flag = 0
option_flag = 0
pickled_memory_file = "testing_phase2.pickle"

while True:
    if mem_flag == 0:
        user_input = input("Welcome to ZUS. I am here to help. Can I start by getting your name?\n")        
    else:
        user_input = input()

    output, summary_value, mem_flag, bot_flag, option_flag, resolution_option = lambda_handler(mem_flag, bot_flag, option_flag,
                                                                pickled_memory_file, user_input)

    print("Bot reply: ", output)
    print("\nChat summary: ", summary_value)
    print("\nResolution option: ", resolution_option)
