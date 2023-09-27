from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Annoy
from langchain.document_loaders import TextLoader


with open('OPENAI_API_KEY/OPENAI_API_KEY_MINDHIVE.txt') as f:
    openai_key = f.readlines()
openai_api_key = str(openai_key[0])


# loader = DirectoryLoader(os.environ['LOAD_DIR'])
loader = TextLoader('db_text/product_menu_clean.txt')
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1500, chunk_overlap=0)
docs = text_splitter.split_documents(documents)
vectordb = Annoy.from_documents(
    documents=docs, 
    embedding=OpenAIEmbeddings(openai_api_key=openai_api_key))

vectordb.save_local("db/products_menu")