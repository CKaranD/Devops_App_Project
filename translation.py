import openai

from get_openai_key import openai_api_key
openai.api_key = openai_api_key

def translator(user_input):
    translate = "Translate the following text to English: "
    all_prompt = translate + user_input

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
