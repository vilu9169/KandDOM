#A summarizer utilising claud
import os
from langchain_google_vertexai import VertexAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain.prompts import ChatPromptTemplate
from langchain_google_vertexai import VertexAI
from langchain.schema.runnable import RunnablePassthrough
from langchain.chains import RetrievalQA

from pinecone import Pinecone, ServerlessSpec, PodSpec  
from langchain_google_vertexai import VertexAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader



from anthropic import AnthropicVertex


def summarise(input, location) -> str:
    # Set the endpoint URL
    context = "Du summerar delar av juridiska dokument som sedan kommer slås samman för att skapa en tidslinje av händelserna i dokumentet. Du ska svara sakligt, opartiskt och enbart använda information från detta dokument i dina svar."  
    #Create a json struct for previous messages and the current message

    client = AnthropicVertex(region=location, project_id="sunlit-inn-417922")

    try:
        message = client.messages.create(
        max_tokens=500,
        model="claude-3-haiku@20240307",
        messages = [{"content": ("Detta är delen av dokumentet du ska summera :" + input), "role": "user"}],
        system = context,
        )
        return message.content[0].text
    except Exception as e:
        print("Error: ", e)
        if(location == "europe-west4"):
            print("retrying in us-central1")
            return summarise(input, "us-central1")
        else:
            print("retrying in europe-west4")
            return summarise(input, "europe-west4")

def summarise_multiple(input, location) -> str:
    # Set the endpoint URL
    context = "Du summerar delar av juridiska dokument som sedan kommer slås samman för att skapa en tidslinje av händelserna i dokumentet. Du ska svara sakligt, opartiskt och enbart använda information från detta dokument i dina svar."  
    #Create a json struct for previous messages and the current message

    client = AnthropicVertex(region=location, project_id="sunlit-inn-417922")
    messages = []
    for elem in input:
        messages.append({"content": ("Detta är delen av dokumentet du ska summera :" + elem.page_content), "role": "user"})
    try:
        message = client.messages.create(
        max_tokens=500,
        model="claude-3-haiku@20240307",
        messages = messages,
        system = context,
        )
        return message.content[0].text
    except Exception as e:
        print("Error: ", e)
        if(location == "europe-west4"):
            print("retrying in us-central1")
            return summarise(input, "us-central1")
        else:
            print("retrying in europe-west4")
            return summarise(input, "europe-west4")


# Load documents
loader = TextLoader("../output.txt", encoding="utf-8")
# Split documents
maxclaudin = 5000
from langchain.text_splitter import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(chunk_size = maxclaudin, chunk_overlap = 0)
splits = text_splitter.split_documents(loader.load())

print("number of splits: ", len(splits))

timelines = []
totind = 0
index = 0
loc = "europe-west4"
# for elem in splits:
#     #Send in 5 splits at a time
#     timelines.append(summarise(elem.page_content, "europe-west4"))
#     loc = "us-central1"
    
#     index += 1
#     if(index == 10):
#         index = 0
#     totind += 1
#     print("totind: ", totind)
# print(timelines)

#Do above but instead send in 5 splits at a time
for i in range(0, len(splits), 5):
    #Send in 5 splits at a time
    timelines.append(summarise_multiple(splits[i:i+5], "us-central1"))
    loc = "europe-west4"
    
    index += 1
    if(index == 10):
        index = 0
    totind += 1
    print("totind: ", totind)


