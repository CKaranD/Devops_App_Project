from lambda_classifier import lambda_classifier
from lambda_conversation_bot import lambda_conversation_bot
from lambda_conversation_bot_vecdb import lambda_conversation_bot_vecdb
from lambda_action_option import lambda_action_option
from lambda_end_of_topic import lambda_end_of_topic


# middleware - set some arguments /values
mem_flag = 0
pickled_memory_file = "testing_phase2.pickle"

# here is the only entry point of user's input, except when asking for order number
if mem_flag == 1:
    user_input = input("Welcome to ZUS. I am here to help. Can I start by getting your name?\n")        
else:
    user_input = input()
    # detect if end of topic, then set flag
    eot_yes_no = lambda_end_of_topic(user_input)

intent = lambda_classifier(user_input)

# middleware if/else rules
if intent != "negative intent":
    # for intents that require zus backend
    if intent == "slow delivery service" or intent == "OOS" or intent == "delivery info / status": 
        order_id = input("May I have your order number please? \n") # middleware to do this
        # with order ID, get status from zus backend(middleware does this), return status
        # may need a mechanism to chekc if order ID is correct
        status = 1 # for debug, we set a value, standardize to use integer
        output, chat_summary = lambda_conversation_bot(mem_flag, pickled_memory_file, user_input, intent, status=0)
        print(output)

        # for intents that need user to select resolution option
        if intent == "slow delivery service" or intent == "OOS":
            # capture the option, and pass to zus backend
            user_option = input()
            output, chat_summary, resolution_option = lambda_action_option(mem_flag, pickled_memory_file, user_option, intent)
            # take the resolution_option and do what ever needed to zus backend
            print(output)

    else: # for intents that use vectorDB
        output, chat_summary = lambda_conversation_bot_vecdb(mem_flag, pickled_memory_file, user_input, intent)
        print(output)

else:
    output, chat_summary = lambda_conversation_bot(mem_flag, pickled_memory_file, user_input, intent, status=0)
    print(output)




# get user_input
# intent = lambda_classifier(user_input)
# middleware
# if intent != "negative intent"
#    intents that require zus backend
#       with order ID, get status(middleware does this), return status
#       output, chat_summary = lambda_conversation_bot(user_input, status) 
#   elif
#       intent rely on vectorDB
#       output = query_db
#       chat_summary = make_summary(chat_history, current_input)
#       if end_of_topic = True 
#       set status = None
# else set status = None
# 
# if bot_flag != 0 and to_answer_option == False
#   option = lambda_action_option