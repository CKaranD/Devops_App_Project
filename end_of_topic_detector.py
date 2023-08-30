import openai
import json
import re

from get_openai_key import openai_api_key
openai.api_key = openai_api_key

template_begin = """. 

You job is to detect if #Input# indicates an end of a conversation. If the #Input# has any elements that is related to either one of the following contexts: 'thanks for your help', 'ok', 'alright', 'good', 'great', 'good to know', 'i see', 'that is all i needed', 'that is all', 'thank you', 'i am good to go', or 'anything that is relevant to the end of a chat', then return 'yes'. Else return 'no'. """

def json_obj_maker(head, customer_input, template):
    asst_prompt = '"' + '#Input# ' + customer_input + template + '"}'
    merged_dict = head + asst_prompt    
    json_obj = json.loads(merged_dict, strict=False)
    return json_obj

def extract_intent(input_string):
    match1 = re.search(r'\byes\b', input_string)    
    if match1:
        return False
    else:
        return True

def EOT_checker(customer_input):    
    translate_table = str.maketrans('"', "'")
    customer_input = customer_input.translate(translate_table)  
    customer_head =  '{"role": "user", "content": '
    
    all_prompt = [
            {"role": "system", "content": "You are an end-of-conversation detector."},
            json_obj_maker(customer_head, customer_input, template_begin)               
            ]

    # Generate a text completion for a given prompt using the "gpt-3.5-turbo" language model
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0,
        max_tokens=8,
        messages=all_prompt,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # get intent
    intent = response['choices'][0]['message']['content']
    # print("pre_level_classifier before filter: ", intent)

    # remove of upper case and full-stop
    intent = intent.lower()
    if '.' in intent:
        intent = intent.replace('.', '')
    if "'" in intent:
        intent = intent.replace("'", '')

    # regex to make sure return intent is exactly from of the labels
    is_negative = extract_intent(intent)
    
    if is_negative == True:
        intent = "no"
    else:
        intent = "yes"

    return intent

# debug script
# customer_input = input()
# intent = EOT_checker(customer_input)
# print(intent)