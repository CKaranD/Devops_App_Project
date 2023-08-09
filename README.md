# ZUSbot Phase 2 Dev + Deployment 

This is Phase 2 of ZUSBOT dev + deployment modules


Lambda Functions' Inputs/Outputs:

lambda_action_option.py

input:
user_input = event['user_input']
intent = event['intent']

output:
{
"resolution_option": resolution_option,
"option_flag": option_flag,
"option_done_flag": option_done_flag
}




lambda_classifier.py

input:
user_input = event['user_input']
output:

{
"intent": pred       
}




lambda_conversation_bot_vecdb.py

input:
mem_flag = event['mem_flag']
pickled_memory_file = event['pickled_memory_file']
user_input = event['user_input']
intent = event['intent']

output:
{
"output": output,
"summary_value": summary_value,
"mem_flag": mem_flag,
"vecdb_flag": vecdb_flag,
"eot_flag": eot_flag  
}



lambda_conversation_bot.py

input:
mem_flag = event['mem_flag']
pickled_memory_file = event['pickled_memory_file']
user_input = event['user_input']
intent = event['intent']
status = event['status']

output:
{
"output": output,
"summary_value": summary_value,
"mem_flag": mem_flag 
}



lambda_end_of_topic.py

input:
customer_input = event['customer_input']
eot_flag = event['eot_flag']
vecdb_flag = event['vecdb_flag']

output:
{
"eot_flag": eot_flag,
"vecdb_flag": vecdb_flag  
}