import openai

with open('OPENAI_API_KEY_MINDHIVE.txt') as f:
    openai_key = f.readlines()
openai_api_key = str(openai_key[0])

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
