import openai

from get_openai_key import openai_api_key
openai.api_key = openai_api_key

def translator(user_input):
    translate = "Translate the following text to English: "
    all_prompt = translate + user_input

    # Using gpt-3.5-turbo model
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a translator."},
            {"role": "user", "content": all_prompt}
        ]
    )

    return response['choices'][0]['message']['content']
