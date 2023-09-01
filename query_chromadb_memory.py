from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory

from get_openai_key import openai_api_key


prompt_template = """As ZUSBot, the customer service chatbot for ZUS Coffee, your role is to respond to customer inquiries based on the information provided in the #Info Sheet#. Ensure your responses are friendly, concise, and cheerful. Avoid making up answers or asking for customer details. If the answer isn't in the #Info Sheet#, creatively express your lack of knowledge.

#Info Sheet#
{context}

{history}
Customer: {question}
ZUSBot:"""

PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["history", "context", "question"]
)

chain_type_kwargs = {"prompt": PROMPT,
                     "memory": ConversationBufferMemory(memory_key="history", input_key="question")}


def get_qa_chain(persist_dir):
    vectordb = Chroma(persist_directory=persist_dir, embedding_function=OpenAIEmbeddings(openai_api_key=openai_api_key))
    retriever = vectordb.as_retriever(search_kwargs={"k": 1}) # define how many documents in the dir
    return RetrievalQA.from_chain_type(
        llm=ChatOpenAI(openai_api_key=openai_api_key, 
                       model_name='gpt-3.5-turbo',
                       temperature=0,
                       max_tokens=512), 
        chain_type="stuff", 
        retriever=retriever,
        chain_type_kwargs=chain_type_kwargs)


##### debugging lines
qa_chain = get_qa_chain('db/outlet_details')
while True:
    user_input = input("Customer: ")
    output = qa_chain.run(user_input)
    print("ZUSBot: ", output)