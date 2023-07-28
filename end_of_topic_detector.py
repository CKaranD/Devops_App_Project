import openai
import json
import re

with open('OPENAI_API_KEY_MINDHIVE.txt') as f:
    key = f.readlines()
openai.api_key = str(key[0])

template_begin = ". Please detect if the above sentence has any elements that is related to something like 'thanks for your help', 'that is all I needed', 'that is all', 'thank you' or 'I am good to go'. Return only 'yes' or 'no'. "

# print("pre negative intent classifier token usage is about: ", len(template_begin)/4)

def json_obj_maker(head, customer_input, template):
    asst_prompt = '"' + customer_input + template + '"}'
    merged_dict = head + asst_prompt    
    json_obj = json.loads(merged_dict)
    return json_obj

def extract_intent(input_string):
    match1 = re.search(r'\byes\b', input_string)    
    if match1:
        return False
    else:
        return True
    

def check_GPT_intent_makeup(intent, patterns):
    for item in patterns:
        if re.search(item, intent):
            return intent
    return "negative intent"

def pre_level_classifier(customer_input):    
    translate_table = str.maketrans('"', "'")
    customer_input = customer_input.translate(translate_table)  
    customer_head =  '{"role": "user", "content": '
    
    all_prompt = [
            {"role": "system", "content": "You are an intent detector."},
            json_obj_maker(customer_head, customer_input, template_begin)               
            ]

    # Generate a text completion for a given prompt using the "gpt-3.5-turbo" language model
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        temperature=0,
        max_tokens=16,
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
        pre_intent = "negative intent"
    else:
        pre_intent = "check further"

    # print("pre_level_classifier: ", pre_intent)
    return pre_intent

# customer_input = input()
# pre_level_classifier(customer_input)