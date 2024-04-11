#A summarizer utilising claud
import os
import time
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

loc = "europe-west4"
model = "claude-3-haiku@20240307"
#model = "claude-3-sonnet@20240229"

def summarise(input):
    global loc
    print("loc: ", loc)
    # Set the endpoint URL
    context = "Skapa en tidslinje baserad på följande dokument. Använd bara information från detta dokument i dina svar. Svara på formatet {time : \"åå-mm-dd hh:mm\", event : \"händelsebeskrivning\"}. Information du inte kan förstå betydelsen av ignorerar du. "  
    #Create a json struct for previous messages and the current message
    client = AnthropicVertex(region=loc, project_id="sunlit-inn-417922")
    try:
        message = client.messages.create(
        max_tokens=1500,
        model=model,
        messages = [{"content": ("Skapa en tidslinje för denna text. Output kommer senare behandlas av ett program och måste därför enbart vara på formatet \"åå-mm-dd hh;mm\" :  \"händelsebeskrivning\". Här är materialet du ska behandla  :" + input), "role": "user"}],
        system = context,
        )
        return message.content[0].text
    except Exception as e:
        print("Error: ", e)
        if(loc == "europe-west4"):
            loc = "us-central1"
            return summarise(input)
        else:
            loc = "europe-west4"
            return summarise(input)
def make_summary(input):
    global loc
    print("loc: ", loc)
    # Set the endpoint URL
    #context = "Du skapar en tidslinje baserad på andra tidslinjer. Du ska vara saklig, opartiskt och enbart använda information från tidslinjerna i dina svar."  
    context = "Du konverterar data till key-value par där nyckeln är datum och värde är associerad händelsetext."
    #Create a json struct for previous messages and the current message

    client = AnthropicVertex(region=loc, project_id="sunlit-inn-417922")

    try:
        message = client.messages.create(
        max_tokens=4096,
        model=model,
        messages = [{"content": ("Behandla denna data :" + input), "role": "user"}],
        system = context,
        )
        return message.content[0].text
    except Exception as e:
        print("Error: ", e)
        if(loc == "europe-west4"):
            loc = "us-central1"
            return make_summary(input)
        else:
            loc = "europe-west4"
            return make_summary(input)
# def summarise_multiple(input, location) -> str:
#     # Set the endpoint URL
#     context = "Du summerar delar av juridiska dokument som sedan kommer slås samman för att skapa en tidslinje av händelserna i dokumentet. Du ska svara sakligt, opartiskt och enbart använda information från detta dokument i dina svar."  
#     #Create a json struct for previous messages and the current message

#     client = AnthropicVertex(region=location, project_id="sunlit-inn-417922")
#     messages = []
#     for elem in input:
#         messages.append({"content": ("Detta är delen av dokumentet du ska summera :" + elem.page_content), "role": "user"})
#     try:
#         message = client.messages.create(
#         max_tokens=500,
#         model="claude-3-haiku@20240307",
#         messages = messages,
#         system = context,
#         )
#         return message.content[0].text
#     except Exception as e:
#         print("Error: ", e)
#         if(location == "europe-west4"):
#             print("retrying in us-central1")
#             return summarise_multiple(input, "us-central1")
#         else:
#             print("retrying in europe-west4")
#             return summarise_multiple(input, "europe-west4")


# Load documents
loader = TextLoader("../Mordforsokgbg.txt", encoding="utf-8")
# Split documents
maxclaudin = 50000
from langchain.text_splitter import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(chunk_size = maxclaudin, chunk_overlap = 0)
splits = text_splitter.split_documents(loader.load())

print("number of splits: ", len(splits))

timelines = []
totind = 0
for elem in splits[:5]:
    #Send in 5 splits at a time
    timelines.append(summarise(elem.page_content))
    totind += 1
    print("totind: ", totind)
megastring = ""
struct = []
for elem in timelines:
    #Drop the first two lines in elem bc these contain garbage from the prompt
    #TODO: Change this to a more robust solution, e.g. by checking if lines are on desired format
    #elem = "\n".join(elem.split("\n")[2:])
    print("TIMELINE: ")
    print(elem)
    megastring += elem
    elem = elem.split("\n")
    for line in elem:
        #Check that line starts with {time, and is not empty, else ignore
        if len(line) > 0 and line[0] == "{" and "time" in line and "event" in line:
            #Events are on the form {time: "2022-03-01 12:00", event: "Event description"}, {time : "22-06-01", event : "DNA-analys slutredovisad."}, extract these
            #Find index of first and second ", and extract the strings between them as time
            ttime = line[line.find("\"")+1:line.find("\"", line.find("\"")+1)]
            #Find index of third ", and extract the substring after this as event
            event = line[line.find("\"", line.find("\"")+1)+1:]
            print("TIME: ", ttime)
            print("EVENT: ", event)
            #Add to struct
            struct.append({"time": ttime, "event": event})
print(struct)
#Turn megastring into a json struct
asjson = {"timeline": struct}
#Summarise megastring
#Note: Denhär fucking suger län
# print("MEGASTRING: "+ make_summary(megastring))



