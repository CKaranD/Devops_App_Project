import openai
import json
import re

from get_openai_key import openai_api_key
openai.api_key = openai_api_key

# template_begin = ". Please classify the above sentence as either #Group A# or 'others'. #Group A# has the following elements: a greeting, 'personal self-introduction', 'thank you', 'that is all', 'sure', 'ok sure', 'ok great', 'good', 'i see', 'got it', 'thats all thank you', 'i do not have phone number', 'a name of someone', farewell, goodbye, and compliment. Return only either #Group A# or 'others' as your answer. "

template_begin = ". Please classify the above sentence as either a greeting, 'personal self-introduction', 'stating thank you / thats all thank you / that is all', 'stating sure / ok sure', 'stating ok / ok great / good', 'a person is telling he/she has no phone /order number', 'asking why order / phone number is needed', 'a name of someone', exclamation, farewell, goodbye, weather, compliment, or 'others'. Return only the exact answer (with exact words and spelling) from the above choices, if there is none to choose from, then return = 'others'. "

# print("pre negative intent classifier token usage is about: ", len(template_begin)/4)

def json_obj_maker(head, customer_input, template):
    asst_prompt = '"' + customer_input + template + '"}'
    merged_dict = head + asst_prompt    
    json_obj = json.loads(merged_dict)
    return json_obj

def extract_intent(input_string):
    match1 = re.search(r'\bothers\b', input_string)
    match2 = re.search(r'\bcompliment\b', input_string)
    if match1 or match2:
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
            {"role": "system", "content": "You are an intent classifier."},
            json_obj_maker(customer_head, customer_input, template_begin)               
            ]

    # Generate a text completion for a given prompt using the "gpt-3.5-turbo" language model
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
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
# print(pre_level_classifier(customer_input))