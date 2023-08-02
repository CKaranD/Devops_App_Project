from lambda_classifier import lambda_classifier
from lambda_conversation_bot import lambda_conversation_bot
from lambda_conversation_bot_vecdb import lambda_conversation_bot_vecdb
from lambda_action_option import lambda_action_option
from lambda_end_of_topic import lambda_end_of_topic

# imagine that the middleware is running as a while loop

# middleware - set some arguments /values
mem_flag = 0 # start as 0 if this is the very first of the conversation
vecdb_flag = 0
eot_flag = 0
option_flag = 0
option_done_flag = 0

# define chat memory pickle file name
pickled_memory_file = "testing_phase2.pickle"


while True: # the following lines are all in the while loop
    # here is the only entry point of user's input, except when asking for order number
    if mem_flag == 0:
        user_input = input("Welcome to ZUS. I am here to help. Can I start by getting your name?\n")        
    else:
        user_input = input("user input: ")
        # detect if end of topic, then set flag, 
        # need a flag to active this line (a flag 
        # that confirms there was an intent that uses vectorDB before this)
        if vecdb_flag == 1:
            eot_yes_no = lambda_end_of_topic(user_input)            
            if eot_yes_no == "yes":
                eot_flag = 1            
                vecdb_flag = 0
    
    if vecdb_flag == 0 and option_flag == 0:
        intent = lambda_classifier(user_input)
        print("intent: ", intent)

    # for intents that need user to select resolution option
    # such as "slow delivery service" or "OOS"
    if option_flag == 1:                       
        resolution_option = lambda_action_option(user_input, intent)
        # take the resolution_option and do what ever needed to zus backend
        print("resolution option: ", resolution_option)
        option_flag = 0
        option_done_flag = 1

    # middleware if/else rules
    if (intent != "negative intent" or eot_flag == 1) and option_done_flag == 0:
        # for intents that require zus backend
        if intent == "slow delivery service" or intent == "OOS" or intent == "delivery info / status": 
            # order_id = input("May I have your order number please? \n") # middleware to do this
            # with order ID, get status from zus backend(middleware does this), return status
            # may need a mechanism to chekc if order ID is correct
            status = 1 # for debug, we set a value, standardize to use integer
            output, chat_summary, mem_flag = lambda_conversation_bot(mem_flag, pickled_memory_file, user_input, intent, status=0)
            print(output)
            option_flag = 1

        # how about intents that have a chain of options
        # most likely use another elif here

        else: # for intents that use vectorDB
            if vecdb_flag == 0 and eot_flag == 1:
                output, chat_summary, mem_flag = lambda_conversation_bot(mem_flag, pickled_memory_file, user_input, intent, status=0)
                print(output)
            else:
                output, chat_summary, mem_flag, vecdb_flag, eot_flag = lambda_conversation_bot_vecdb(mem_flag, pickled_memory_file, user_input, intent)        
                print(output)

    else:
        output, chat_summary, mem_flag = lambda_conversation_bot(mem_flag, pickled_memory_file, user_input, intent, status=0)
        print(output)
        option_done_flag = 0



# =============== Documentation about flags =============== #
#
# mem_flag => to decide the creation / loading of chat memory
#
# vecdb_flag => to check if previously there was a call to lambda_conversation_bot_vecdb()
#               hence the need of activating lambda_end_of_topic() to check if there is a
#               follow-up inquiry
#
# eot_flag => to check if end of topic is true
#
# option_flag => to check if there is a need to trigger lambda_action_option() 
#                to capture user's resolution option
#
# option_done_flag => to inform the flow that resolution option is captured 
#                     and exit into the relevant juncture