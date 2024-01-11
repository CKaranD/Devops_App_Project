import openai

from detect_language import detect_language
from get_openai_key import openai_api_key
openai.api_key = openai_api_key


def translator(sys_msg, language):
    translate = "Translate the following text to " + language + ": "
    all_prompt = translate + sys_msg

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a translator."},
            {"role": "user", "content": all_prompt}
        ]
    )

    return response['choices'][0]['message']['content']


def response_system_msg(user_input, sys_msg):
    language = detect_language(user_input)

    if language != "English":
        out_msg = translator(sys_msg, language)
        out_msg = out_msg.replace("\n", " ")
    else:
        out_msg = sys_msg

    return out_msg