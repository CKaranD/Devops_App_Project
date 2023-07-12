import os
from zusbot_main_no_tools import *
from json_object_maker import create_json_object
from detect_language import detect_language
from mlp_classifier import mlp_classifier
from pre_negative_intent_classifier import pre_level_classifier
from translation import translator
from levenshtein_options_checking import check_closer_option

def lambda_handler(event, context):
    # Set MPLCONFIGDIR to /tmp
    os.environ['MPLCONFIGDIR'] = '/tmp'
    
    mem_flag = event['mem_flag']
    bot_flag = event['bot_flag']
    option_flag = event['option_flag']
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
    
    # conversation
    if pred == "slow delivery service":
        from template_sub_slow_delivery_service import (ZUS_LANGUAGE_INSTRUCTIONS, ZUS_PREFIX, ZUS_SUFFIX)
        ZUS_TEMPLATE = ZUS_PREFIX + ZUS_LANGUAGE_INSTRUCTIONS + language + ZUS_SUFFIX        
        order_num = input("May I have your order number please? \n")
        # verify if the number is valid, and do some backend proces with order_num
        output, summary_value = zusbot(ZUS_TEMPLATE, llm, user_input, memory, pickled_memory_file)
        bot_flag = 1 # set bot_flag

    elif pred == "OOS":
        from template_sub_oos import (ZUS_LANGUAGE_INSTRUCTIONS, ZUS_PREFIX, ZUS_SUFFIX)
        ZUS_TEMPLATE = ZUS_PREFIX + ZUS_LANGUAGE_INSTRUCTIONS + language + ZUS_SUFFIX        
        order_num = input("May I have your order number please? \n")
        # verify if the number is valid, and do some backend proces with order_num
        output, summary_value = zusbot(ZUS_TEMPLATE, llm, user_input, memory, pickled_memory_file)
        bot_flag = 2 # set bot_flag

    # add more of such rule here for other intents, 
    # may need to re-organize their sequence and bot_flag for better visual
    else:
        from template_main_v4 import (ZUS_LANGUAGE_INSTRUCTIONS, ZUS_PREFIX, ZUS_SUFFIX)
        ZUS_TEMPLATE = ZUS_PREFIX + ZUS_LANGUAGE_INSTRUCTIONS + language + ZUS_SUFFIX
        output, summary_value = zusbot(ZUS_TEMPLATE, llm, user_input, memory, pickled_memory_file)
    
    # output, summary_value = zusbot(ZUS_TEMPLATE, llm, user_input, memory, pickled_memory_file)

    # check bot_flag, and get user's response
    if bot_flag == 0:
        resolution_option = "None"
    
    # slow delivery service
    elif bot_flag == 1:
        resolution_option = "None"
        option_flag += 1
        if option_flag >= 2:
            options = [
                "option (a): Cancel the order with a refund",
                "option (b): Take the 'ZUSSORRY' voucher"
            ]
            resolution_option = check_closer_option(user_input, options)            
    
    # OOS
    elif bot_flag == 2:
        resolution_option = "None"
        option_flag += 1
        if option_flag >= 2:
            options = [
                "option (a): Cancel the order with full refund",
                "option (b): Take partial refund"
            ]
            resolution_option = check_closer_option(user_input, options)            

    json_obj = create_json_object(output, summary_value, mem_flag, bot_flag, option_flag, resolution_option)
    
    return json_obj