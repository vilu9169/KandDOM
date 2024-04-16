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

# print(res)

from anthropic import AnthropicVertex


def ragadapt(input, previous_messages) -> str:
    # Set the endpoint URL
    MODEL="claude-3-haiku@20240307"
    endpoint = f"https://us-central1-aiplatform.googleapis.com/v1/projects/sunlit-inn-417922/locations/europe-west4/publishers/anthropic/models/"+MODEL+":predict"
    context = "Your purpose is to expand the users latest question. Short questions should be reasked in multiple ways and if there is relevant context available from previous messages use that context to expand the question. If you cant do anything relevant with the question just send it back as is" 
    #Create a json struct for previous messages and the current message
    messages = []
    odd = True
    for message in previous_messages:
        if odd:
            messages.append({
                "role": "user",
                "content": message
            })
            odd = False
        else:
            messages.append({
                "role": "assistant",
                "content": message
            })
            odd = True
    messages.append({
        "role": "user",
        "content": "Expand this question \" " +input + "\" and only answer with expansions of the question. Other text in the answer is strictly forbidden."
    })

    LOCATION="europe-west4"

    client = AnthropicVertex(region=LOCATION, project_id="sunlit-inn-417922")

    message = client.messages.create(
    max_tokens=300,
    messages=messages,
    model="claude-3-haiku@20240307",
    #model = "claude-3-sonnet@20240229",
    system = context,
    )
    print("Improved text", message.content[0].text)
    return message.content[0].text







def start_chat(input, previous_messages) -> str:
    print("Starting chat")
    # Set the endpoint URL
    #MODEL="claude-3-haiku@20240307"
    MODEL = "claude-3-sonnet@20240229"
    
    endpoint = f"https://us-central1-aiplatform.googleapis.com/v1/projects/sunlit-inn-417922/locations/europe-west4/publishers/anthropic/models/"+MODEL+":predict"
    context = "Du analyserar juridiska dokument för att underlätta arbete med dem. Du ska svara sakligt, opartiskt och enbart använda information från detta dokument i dina svar. Detta är de delar av dokument du har att tillgå :" 
    index = 0
    prepend = ""
    append = ""
    for rag in vectorstore.as_retriever(search_type="mmr", search_kwargs = ({"k" : 60, })).invoke(ragadapt(input, previous_messages)):
        #The first 10 documents are prepended to the context
        #The last 10 documents are appended to append
        if index < 10:
            prepend += rag.page_content
        elif index >10 and index < 20:
            append = rag.page_content + append
        else:
            prepend += rag.page_content
        index += 1
        #Extract text from document
    context += prepend + append
    #print("Context: ", context)
    print("Rag done")
    #Create a json struct for previous messages and the current message
    messages = []
    odd = True
    for message in previous_messages:
        if odd:
            messages.append({
                "role": "user",
                "content": message
            })
            odd = False
        else:
            messages.append({
                "role": "assistant",
                "content": message
            })
            odd = True
    messages.append({
        "role": "user",
        "content": input
    })

    LOCATION="europe-west4"

    client = AnthropicVertex(region=LOCATION, project_id="sunlit-inn-417922")

    message = client.messages.create(
    max_tokens=500,
    messages=messages,
    model="claude-3-haiku@20240307",
    system = context,
    )
    return message.content[0].text



# Call the function with your project ID and location
prevmessages = []
while(True):
    #Prompt user for input
    print("Enter your message: ")
    message = input()
    res = start_chat(message, prevmessages)
    prevmessages.append(message)
    prevmessages.append(res)
    print(res)


