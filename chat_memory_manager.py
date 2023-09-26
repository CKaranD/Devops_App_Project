import requests
import json

from zus_write_load_mem import write_memory

with open('OPENAI_API_KEY_MINDHIVE.txt') as f:
    key = f.readlines()
API_KEY = str(key[0])
API_ENDPOINT = "https://api.openai.com/v1/chat/completions"

def generate_chat_completion(prompt, 
                             model="gpt-3.5-turbo", 
                             temperature=1, 
                             max_tokens=None):
    
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    }

    data = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
    }

    if max_tokens is not None:
        data["max_tokens"] = max_tokens

    response = requests.post(API_ENDPOINT, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")


# response_text = generate_chat_completion(messages)
# print(response_text)

def memory_manager(memory, pickled_memory_file, user_input, sys_msg):
    
    summary = memory.memories[-1].buffer    

    p1 = """Given a chat history and conversation snippet between a customer and ZUSBot, a ZUS Coffee chatbot. """
    p2 = """Chat History: 
    """
    p3 = """Conversation Snippet: 
    Customer says to ZUSBot: """
    p4 = """
    ZUSBot says to the Customer: """
    p5 = """
    
    Please summarize the chat history and the conversation snippet into a short summary. The summary summarizes the paragraph whilst retaining all important information such as, but not limited to, past customer issues, past resolutions, past notable bot replies, interaction dates and customer sentiment. The summary must remember the Customer's name (if no name is found, then omit addressing the Customer), and extract ALL important information that enables ZUSBot to respond in a way that makes the customer feel valued at ZUS Coffee. Your answer here: """

    prompt = p1 + p2 + summary + p3 + user_input + p4 + sys_msg + p5

    # prompt = """Your job is to summarize and append based on the following instruction. \n\n#CHAT_EXTRACT# is a summary of conversation between a customer and ZUSBot. ZUSBot is ZUS Coffee's chatbot and it addresses various customer issues. \nSummarize the following #INPUT# and now it is known as #NEW_SUMMARY#. You must remember the Customer's name, and include the Customer's name into the #NEW_SUMMARY#. Now, append #NEW_SUMMARY# to the end of #CHAT_EXTRACT#. \n\n#INPUT# \nCustomer says to ZUSBot: """ + user_input + """\nZUSBot says to the Customer: """ + sys_msg + """\n\n#CHAT_EXTRACT# \n""" + summary + """ \n\nREMEMBER to append the #NEW_SUMMARY# to the end of #CHAT_EXTRACT# \n\nNow return ONLY the latest contents of #CHAT_EXTRACT# here:"""
    
    final_summary = generate_chat_completion(prompt)

    memory.memories[-1].buffer = final_summary
    
    # upload memory to AWS S3        
    write_memory(memory, pickled_memory_file)

    return final_summary

