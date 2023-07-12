import os
from zusbot_main_no_tools import *
from json_object_maker import create_json_object
from detect_language import detect_language
from mlp_classifier import mlp_classifier
from pre_negative_intent_classifier import pre_level_classifier
from translation import translator
from levenshtein_options_checking import levenshtein_distance, check_closer_option

def lambda_handler(mem_flag, bot_flag, option_flag, pickled_memory_file, user_input):
    # Set MPLCONFIGDIR to /tmp
    # os.environ['MPLCONFIGDIR'] = '/tmp'    
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
    if pred == "negative intent" or pred != "slow delivery service":
        from template_main_v4 import (ZUS_LANGUAGE_INSTRUCTIONS, ZUS_PREFIX, ZUS_SUFFIX)
        ZUS_TEMPLATE = ZUS_PREFIX + ZUS_LANGUAGE_INSTRUCTIONS + language + ZUS_SUFFIX
        # output, summary_value = zusbot(ZUS_TEMPLATE, llm, user_input, memory, pickled_memory_file)
        
    elif pred == "slow delivery service":
        from template_sub_slow_delivery_service import (ZUS_LANGUAGE_INSTRUCTIONS, ZUS_PREFIX, ZUS_SUFFIX)
        ZUS_TEMPLATE = ZUS_PREFIX + ZUS_LANGUAGE_INSTRUCTIONS + language + ZUS_SUFFIX        
        order_num = input("Bot reply: May I have your order number please? \n")
        # verify if the number is valid, and do some backend proces with order_num        
        # output, summary_value = zusbot(ZUS_TEMPLATE, llm, user_input, memory, pickled_memory_file)
        bot_flag = 1 # set bot_flag

    # add more of such rule here for other intents
    
    output, summary_value = zusbot(ZUS_TEMPLATE, llm, user_input, memory, pickled_memory_file)

    # check bot_flag, and get user's response
    if bot_flag == 0:
        ner = ""
    elif bot_flag == 1:
        option_flag += 1
        if option_flag >= 2:
            options = [
                "option (a): Cancel the order with a refund",
                "option (b): Take the 'ZUSSORRY' voucher"
            ]
            result = check_closer_option(user_input, options)
            print(result)

    # json_obj = create_json_object(user_input, output, summary_value, mem_flag)

    return output, summary_value, mem_flag, bot_flag, option_flag



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

    output, summary_value, mem_flag, bot_flag, option_flag = lambda_handler(mem_flag, bot_flag, option_flag,
                                                                pickled_memory_file, user_input)

    print("Bot reply: ", output)
    print("chat summary: ", summary_value)
