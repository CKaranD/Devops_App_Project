with open('OPENAI_API_KEY_MINDHIVE.txt') as f:
    key = f.readlines()
openai_api_key = str(key[0])