from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA

from get_openai_key import openai_api_key

def get_qa_chain(persist_dir):
    vectordb = Chroma(persist_directory=persist_dir, embedding_function=OpenAIEmbeddings(openai_api_key=openai_api_key))
    retriever = vectordb.as_retriever(search_kwargs={"k": 1}) # define how many documents in the dir
    return RetrievalQA.from_chain_type(
        llm=ChatOpenAI(openai_api_key=openai_api_key, 
                       temperature=0,
                       max_tokens=512), 
        chain_type="stuff", 
        retriever=retriever)


# qa_chain = get_qa_chain('db/loyalty_benefits')
# while True:
#     user_input = input("Customer: ")
#     output = qa_chain.run(user_input)
#     print("ZUSBot: ", output)