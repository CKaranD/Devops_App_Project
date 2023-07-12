import json

def create_json_object(input_text, output_text, summary, mem_flag):
    data = {
        "input": input_text,
        "output": output_text,
        "summary": summary,        
        "mem_flag": mem_flag        
    }
    json_object = json.dumps(data)
    return json_object

# input_text = "I am Jermaine"
# output_text = "Hi Jermaine! Welcome to ZUS Coffee. How may I assist you today?"
# summary = "A customer named Jermaine introduces themselves to ZUSBot at ZUS Coffee and the bot greets them and asks how it can assist."
# intent = "negative intent"
# confidence = 0.9998732909046618
# mem_flag = 1

# json_obj = create_json_object(input_text, output_text, summary, intent, confidence, mem_flag)
# print(json_obj)