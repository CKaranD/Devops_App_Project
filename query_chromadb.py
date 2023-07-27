from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA

with open('OPENAI_API_KEY_MINDHIVE.txt') as f:
    openai_key = f.readlines()
openai_api_key = str(openai_key[0])

def get_qa_chain():
    vectordb = Chroma(persist_directory='.', embedding_function=OpenAIEmbeddings(openai_api_key=openai_api_key))
    retriever = vectordb.as_retriever(search_kwargs={"k": 1}) # define how many documents in the dir
    return RetrievalQA.from_chain_type(
        llm=ChatOpenAI(openai_api_key=openai_api_key, temperature=0), 
        chain_type="stuff", 
        retriever=retriever)

qa_chain = get_qa_chain()
user_input = input("Yor query: ")
output = qa_chain.run(user_input)
print(output)