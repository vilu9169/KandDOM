import getpass
import os

#os.environ["OPENAI_API_KEY"] = getpass.getpass("OpenAI API Key:")

import getpass

#MONGODB_ATLAS_CLUSTER_URI = getpass.getpass("MongoDB Atlas Cluster URI:")

from pymongo import MongoClient

# initialize MongoDB python client
client = MongoClient(MONGODB_ATLAS_CLUSTER_URI)

# DB_NAME = "langchain_db"
# COLLECTION_NAME = "test"
# ATLAS_VECTOR_SEARCH_INDEX_NAME = "index_name"

# MONGODB_COLLECTION = client[DB_NAME][COLLECTION_NAME]


from langchain_community.document_loaders import PyPDFLoader

# Load the PDF
loader = PyPDFLoader("/home/calle/skola/KandDOM/backend/tointegrate")
data = loader.load()


from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
docs = text_splitter.split_documents(data)

print(docs[0])

from langchain_community.vectorstores import MongoDBAtlasVectorSearch
from langchain_google_vertexai import VertexAIEmbeddings

# insert the documents in MongoDB Atlas with their embedding
vector_search = MongoDBAtlasVectorSearch.from_documents(
    documents=docs,
    embedding=VertexAIEmbeddings(disallowed_special=()),
    collection=MONGODB_COLLECTION,
    index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME,
)

# Perform a similarity search between the embedding of the query and the embeddings of the documents
query = "What were the compute requirements for training GPT 4"
results = vector_search.similarity_search(query)

print(results[0].page_content)