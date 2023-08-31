import pickle
import re
    
import openai
from langchain import LLMChain
from langchain.chains import (ConversationChain, ConversationalRetrievalChain)
from langchain.chat_models import ChatOpenAI
from langchain.memory import (CombinedMemory, ConversationBufferMemory,
                            ConversationSummaryMemory)    
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma

# from template_main_v4 import (ZUS_LANGUAGE_INSTRUCTIONS, ZUS_PREFIX,
#                                 ZUS_SUFFIX)
from langchain.prompts import PromptTemplate

from zus_write_load_mem import write_memory, load_memory



# def keygen():    
#     with open('OPENAI_API_KEY_MINDHIVE.txt') as f:
#         openai_key = f.readlines()
#     openai_api_key = str(openai_key[0])
    
#     return openai_api_key


def create_llm(openai_api_key):
    llm=ChatOpenAI(openai_api_key=openai_api_key, 
            model_name='gpt-3.5-turbo',
            temperature=0,
            max_tokens = 2048)
    return llm


def create_memory(llm):
    # define the memory sets
    conv_memory = ConversationBufferMemory(
        memory_key="chat_history_lines",
        input_key="input", 
        return_messages=True,
        human_prefix="Customer",
        ai_prefix="ZUSBot")

    summary_memory = ConversationSummaryMemory(llm=llm, input_key="input", 
                                               memory_key="history",
                                               human_prefix="Customer",
                                               ai_prefix="ZUSBot")
    memory = CombinedMemory(memories=[conv_memory, summary_memory])
    return memory


def is_dialogue_01(text):
    customer_start = text.find("Customer:")
    customer_end = text.rfind("Customer:")
    bot_start = text.find("ZUSBot:")
    bot_end = text.rfind("ZUSBot:")
    
    if customer_start == -1 or customer_end == -1 or bot_start == -1 or bot_end == -1:
        return False
    else:
        return True
    
def is_dialogue_02(text):
    # Define regular expressions for common dialogue structures
    dialogue_patterns = [
        r'^\s*\w+:',  # Pattern for "Speaker: Text" format        
        r'^\s*\w+\s*\(.+\):\s*',  # Pattern for "Speaker (descriptor): Text" format
        r'^\s*\w+\s*\(.+\)\s*$',  # Pattern for "Speaker (descriptor)" format
        r'^\s*-+\s*$',  # Pattern for divider lines
    ]
    
    # Check if any of the patterns match any of the lines in the text    
    for line in text.split('\n'):
        if not any(re.match(p, line) for p in dialogue_patterns):
            return False
        else:
            return True


def extract_response(text):
    patterns = [r'ZUSBot: (.*)', r'ZUSBot:(.*)']
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            response = match.group(1) 
        else:
            response = text  
    return response


def zusbot(ZUS_TEMPLATE, llm, user_input, memory, pickled_memory_file):
    PROMPT = PromptTemplate(
    input_variables=["history", "input", "chat_history_lines"], template=ZUS_TEMPLATE)

    # LLM chain consisting of the LLM and a prompt
    llm_chain = ConversationChain(
                llm=llm, 
                verbose=False, 
                memory=memory,
                prompt=PROMPT
            )
    
    output = llm_chain.run(input=user_input)

    is_dialg1 = is_dialogue_01(output)
    is_dialg2 = is_dialogue_02(output)

    if is_dialg2 == True:
        filtered_output = extract_response(output)
    elif is_dialg1 == True:
        filtered_output = output.splitlines()[0]
    else:
        filtered_output = output
    
    if is_dialg1 == True or is_dialg2 == True:        
        memory.memories[0].chat_memory.messages[1].content = filtered_output
        memory.memories[1].chat_memory.messages[1].content = filtered_output
        memory.memories[-1].buffer = "A customer introduces themselves to ZUSBot and asks for assistance."
    
    summary_value = memory.memories[-1].buffer
    
    # upload memory to AWS S3        
    write_memory(memory, pickled_memory_file)

    return filtered_output, summary_value


def zusbot_vectordb(ZUS_TEMPLATE, intent, output_qa, llm, user_input, memory, pickled_memory_file):
    PROMPT = PromptTemplate(
    input_variables=["history", "input", "chat_history_lines"], template=ZUS_TEMPLATE)

    # LLM chain consisting of the LLM and a prompt
    llm_chain = ConversationChain(
                llm=llm, 
                verbose=False, 
                memory=memory,
                prompt=PROMPT
            )
    
    output = llm_chain.run(input=user_input)

    is_dialg1 = is_dialogue_01(output)
    is_dialg2 = is_dialogue_02(output)

    if is_dialg2 == True:
        filtered_output = extract_response(output)
    elif is_dialg1 == True:
        filtered_output = output.splitlines()[0]
    else:
        filtered_output = output
    
    if is_dialg1 == True or is_dialg2 == True:        
        memory.memories[0].chat_memory.messages[1].content = filtered_output
        memory.memories[1].chat_memory.messages[1].content = filtered_output
        memory.memories[-1].buffer = "A customer introduces themselves to ZUSBot and asks for assistance."
    # replace the currently generated output with retrieval output         
    memory.memories[0].chat_memory.messages[-1].content = output_qa
    memory.memories[1].chat_memory.messages[-1].content = output_qa

    # need to help with the shorten summary, 
    # else the retrieval returns is too lengthy and cause token limit issue
    if intent == "loyalty benefits":
        memory.memories[-1].buffer += " The customer asks information about loyalty benefits, and ZUSBot provides some info."
    elif intent == "product / menu details":
        memory.memories[-1].buffer += " The customer asks information about a ZUS product, and ZUSBot provides some info."
    elif intent == "birthday / vouchers":
        memory.memories[-1].buffer += " The customer asks information about vouchers or a birthday voucher, and ZUSBot provides some info."
    elif intent == "outlet details":
        memory.memories[-1].buffer += " The customer asks information about outlet details, and ZUSBot provides some info."
    # add more rules here, remember the 1 space before the injected summary fraction
    
    summary_value = memory.memories[-1].buffer

    # upload memory to AWS S3        
    write_memory(memory, pickled_memory_file)

    return filtered_output, summary_value