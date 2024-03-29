# Adapt the following tutorials to use Vertex AI embeddings
# from https://python.langchain.com/docs/integrations/vectorstores/pinecone
# and https://python.langchain.com/docs/use_cases/question_answering/


import os
import getpass

#os.environ["PINECONE_API_KEY"] = getpass.getpass("Pinecone API Key:")
os.environ["PINECONE_API_KEY"] = "2e669c83-1a4f-4f19-a06a-42aaf6ea7e06"
os.environ["PINECONE_ENV"] = "default"

from langchain_google_vertexai import VertexAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader


# Load documents
loader = TextLoader("D:/Plugg/Kandarb/KandDOM/backend/tointegrate/output.txt", encoding="utf-8")
# Split documents

from langchain.text_splitter import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap = 0)
splits = text_splitter.split_documents(loader.load())

embeddings = VertexAIEmbeddings(model_name="textembedding-gecko-multilingual@001")
from pinecone import Pinecone, ServerlessSpec

pc = Pinecone(
    api_key=os.environ.get("PINECONE_API_KEY"),
    environment=os.getenv("PINECONE_ENV"),  # next to api key in console
        
)
# initialize pinecone
index_name = "langchain-demo"

# First, check if our index already exists. If it doesn't, we create it
# Now do stuff
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=1536,
        metric='euclidean',
        spec=ServerlessSpec(
            cloud='aws',
            region='us-west-2'
        )
    )

#vectorstore = Pinecone(index_name, embeddings.embed_query, splits)
print("past index creation for index ", index_name)
# Vertex AI embedding model  uses 768 dimensions`
vectorstore = pc.from_documents(splits, embeddings, index_name=index_name)

retriever = vectorstore.as_retriever()

# Prompt 
# https://smith.langchain.com/hub/rlm/rag-prompt

from langchain import hub
rag_prompt = hub.pull("rlm/rag-prompt")

print("past index rag_prompt creation ")
from langchain.prompts import ChatPromptTemplate
from langchain.llms import VertexAI
llm = VertexAI()
 

# RAG chain 

from langchain.schema.runnable import RunnablePassthrough
rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()} 
    | rag_prompt 
    | llm 
)

rci_output = rag_chain.invoke("What is Task Decomposition?")
print("rci_output is: ",rci_output)