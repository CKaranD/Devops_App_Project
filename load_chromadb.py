import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.document_loaders import TextLoader

from dotenv import load_dotenv
load_dotenv()

with open('OPENAI_API_KEY/OPENAI_API_KEY_MINDHIVE.txt') as f:
    openai_key = f.readlines()
openai_api_key = str(openai_key[0])

if not (os.path.exists('chroma-collections.parquet') and os.path.exists('chroma-embeddings.parquet')):
    # loader = DirectoryLoader(os.environ['LOAD_DIR'])
    loader = TextLoader('db_text/merged_birthday_vouchers_loyalty_benefits.txt')
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)
    vectordb = Chroma.from_documents(
        documents=docs, 
        embedding=OpenAIEmbeddings(openai_api_key=openai_api_key), 
        persist_directory='db/birthday_vouchers')
    vectordb.persist()