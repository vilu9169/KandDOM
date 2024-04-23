from langchain.vectorstores import Pinecone
from langchain_pinecone import PineconeVectorStore
from langchain_google_vertexai import VertexAIEmbeddings
import os
from dotenv import load_dotenv
load_dotenv()

embd = VertexAIEmbeddings("textembedding-gecko-multilingual@001")

model = 

pc = Pinecone(api_key= os.getenv('PINECONE_API_KEY'))
index = pc.Index("raptor")

vectorstore = PineconeVectorStore(index="raptor", embedding=embd.embed_query)


retriever = vectorstore.as_retriever()




from langchain import hub
from langchain_core.runnables import RunnablePassthrough

# Prompt
prompt = hub.pull("rlm/rag-prompt")


# Post-processing
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


# Chain
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
)

# Question
rag_chain.invoke("")