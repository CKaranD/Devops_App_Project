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



def keygen():    
    with open('OPENAI_API_KEY_MINDHIVE.txt') as f:
        openai_key = f.readlines()
    openai_api_key = str(openai_key[0])
    
    return openai_api_key


def create_llm(openai_api_key):
    llm=ChatOpenAI(openai_api_key=openai_api_key, 
            model_name='gpt-3.5-turbo-0613',
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


def zusbot(ZUS_TEMPLATE, llm, user_input, memory, pickled_memory_file, is_retrieval_qa=False, retrival_db=None):
    if(is_retrieval_qa):

        openai_api_key = keygen()
        vectordb = Chroma(persist_directory=retrival_db, embedding_function=OpenAIEmbeddings(openai_api_key=openai_api_key))
        retriever = vectordb.as_retriever()

        llm_chain = ConversationalRetrievalChain.from_llm(
            llm=ChatOpenAI(openai_api_key=openai_api_key, 
                            temperature=0, 
                            model="gpt-3.5-turbo-16k-0613"
                        ), 
            chain_type="stuff", 
            retriever=retriever,
            memory=memory,
            verbose=False)
        
        # Need Sifu KY's help, cannot seems to get the chat_history_lines to work
        # error: KeyError: 'input
        output = llm_chain.run(question=user_input,chat_history=[])
        
    else:
        # ZUS_TEMPLATE = ZUS_PREFIX + ZUS_LANGUAGE_INSTRUCTIONS + language + ZUS_SUFFIX
        
        PROMPT = PromptTemplate(
        input_variables=["history", "input", "chat_history_lines"], template=ZUS_TEMPLATE)        

        # LLM chain consisting of the LLM and a prompt
        llm_chain = ConversationChain(
                    llm=llm, 
                    verbose=True, 
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