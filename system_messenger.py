import openai

from detect_language import detect_language
from get_openai_key import openai_api_key
openai.api_key = openai_api_key


def translator(sys_msg, language):
    translate = "Translate the following text to " + language + ": "
    all_prompt = translate + sys_msg
    
    response = openai.Completion.create(
    model="text-davinci-003",
    prompt = all_prompt,    
    temperature=0,
    max_tokens=1024,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )

    return response.choices[0].text


def response_system_msg(user_input, sys_msg):
    language = detect_language(user_input)

    if language != "English":
        out_msg = translator(sys_msg, language)
        out_msg = out_msg.replace("\n", " ")
    else:
        out_msg = sys_msg

    return out_msg