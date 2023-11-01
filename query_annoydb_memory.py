from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Annoy
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.memory import (CombinedMemory, ConversationBufferMemory,
                            ConversationSummaryMemory) 

from get_openai_key import openai_api_key

# If there is no relevant information found in Context, you MUST say that you don't know, NEVER make up an answer. For sensitive food safety or food allergy related issues (e.g. lactose intolerance, gluten intolerance or diabetic).If drink contains dairy milk, it is not suitable for lactose intolerant people. If drink contains sugar, it is not suitable for diabetic people. If you are not sure about dietary requirements, you MUST refer the customer to a nutritionists or dietitian.
# Do not ask for Customer's details. Do not commit actions.

prompt_template = """You are ZUS Coffee's customer service chatbot known as ZUSBot - Lydia. The Customer is inquiring about some information from ZUSBot - Lydia. ZUSBot - Lydia's objective is to use the information in Context to answer the inquiry of the Customer. ZUSBot must reply exclusively based on the information from Context only.
ZUSBot must search recursively within all the Context to provide an extremely complete response to the customer. If there is no relevant information found in Context, you MUST say that you don't know, NEVER make up an answer and do not hallucinate. 

If customer asks about outlet, drinks, food, pastries, cakes, promotions, vouchers, without specifying any specifics, reply with a followup question. But if customer had prior reference, you must remember that and do not assume. If there are multiple options, return all.

eg: Customer says "outlet open what time", you would need to ask "Which outlet are you referring to?".

Context:
{context}

To place orders, ZUSBot directs customers to ZUS Coffee Mobile App.

Summary of conversation:
{history}

Current conversation:
{chat_history_lines}

Customer: {question}
ZUSBot:"""


def create_query_memory():
    llm=ChatOpenAI(openai_api_key=openai_api_key, 
            model_name='gpt-3.5-turbo',
            temperature=0.6,
            max_tokens = 2048)
    
    conv_memory = ConversationBufferMemory(
        memory_key="chat_history_lines",
        input_key="question", 
        return_messages=True,
        human_prefix="Customer",
        ai_prefix="ZUSBot")

    summary_memory = ConversationSummaryMemory(llm=llm, input_key="question", 
                                               memory_key="history",
                                               human_prefix="Customer",
                                               ai_prefix="ZUSBot")
    memory = CombinedMemory(memories=[conv_memory, summary_memory])
    # memory = ConversationBufferMemory(memory_key="history", input_key="question")
    return memory


def get_qa_chain(db_dir, memory):

    PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["history", "chat_history_lines", "context", "question"]
    )

    chain_type_kwargs = {"prompt": PROMPT,
                        "memory": memory}

    vectordb = Annoy.load_local(db_dir, embeddings=OpenAIEmbeddings(openai_api_key=openai_api_key))    
    retriever = vectordb.as_retriever(search_kwargs={"k": 1}) # define how many documents in the dir

    ans = RetrievalQA.from_chain_type(
            llm=ChatOpenAI(openai_api_key=openai_api_key, 
                        model_name='gpt-3.5-turbo',
                        temperature=0.3,
                        max_tokens=1650), 
            chain_type="stuff", 
            retriever=retriever,
            chain_type_kwargs=chain_type_kwargs)

    return ans, memory

#search_type="mmr", search_kwargs={'k': 5, 'fetch_k': 50}


##### debugging lines
# memory = create_query_memory()
# qa_chain, memory = get_qa_chain('db/loyalty_benefits', memory)
# while True:
#     user_input = input("Customer: ")
#     output = qa_chain.run(user_input)
#     print("ZUSBot: ", output)
#     print("memory: ", memory)

