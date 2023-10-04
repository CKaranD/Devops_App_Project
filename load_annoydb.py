from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Annoy
from langchain.document_loaders import TextLoader


with open('OPENAI_API_KEY/OPENAI_API_KEY_MINDHIVE.txt') as f:
    openai_key = f.readlines()
openai_api_key = str(openai_key[0])


# loader = DirectoryLoader(os.environ['LOAD_DIR'])

loader = TextLoader('db_text/outlet_details_clean.txt')
# loader = TextLoader('db_text/outlet_details_clean.txt')
# loader = TextLoader('db_text/combined_loyalty_benefit_birthday_voucher.txt')

documents = loader.load()

#product_menu_clean: chunk size 1800, overlap 0
#outlet_details_clean: chunk size 1000, overlap 0
# combined_loyalty_benefit_birthday_voucher: chunk size 1800, overlap 0

text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)

docs = text_splitter.split_documents(documents)
vectordb = Annoy.from_documents(
    documents=docs, 
    embedding=OpenAIEmbeddings(openai_api_key=openai_api_key))

# vectordb.save_local("db/products_menu")
vectordb.save_local("db/outlet_details")

# vectordb.save_local("db/birthday_vouchers")
# vectordb.save_local("db/loyalty_benefits")