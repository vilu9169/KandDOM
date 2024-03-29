import os
from langchain_google_vertexai import VertexAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain.prompts import ChatPromptTemplate
from langchain_google_vertexai import VertexAI
from langchain.schema.runnable import RunnablePassthrough
from langchain.chains import RetrievalQA


from pinecone import Pinecone, ServerlessSpec, PodSpec  

pc = Pinecone(api_key="2e669c83-1a4f-4f19-a06a-42aaf6ea7e06")
index_name = "langchain-demo"
index = pc.Index(index_name)  
#print(index.describe_index_stats())

embeddings = VertexAIEmbeddings(model_name="textembedding-gecko-multilingual@001")

from langchain_pinecone import PineconeVectorStore  
#Load document text from file
# with open(FIlE_PATH, "r", encoding="utf-8") as f:
#     text_field = f.read()
vectorstore = PineconeVectorStore(  
    index, embeddings  
)  
llm = VertexAI()
from langchain import hub
rag_prompt = hub.pull("rlm/rag-prompt")
from langchain.schema.runnable import RunnablePassthrough
qa = RetrievalQA.from_chain_type(  
    llm=llm,  
    chain_type="stuff",  
    retriever=vectorstore.as_retriever(search_type="mmr", k=5),  
)  
res = qa.invoke("Vilka är vittnen i fallet?") 


print(res)
