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
    context = "Skapa en tidslinje baserad på följande dokument. Använd bara information från detta dokument i dina svar och upprepa dig inte. Svara på formatet {time : \"åååå-mm-dd hh:mm\", event : \"händelsebeskrivning\"}. Händelsebeskrivningen ska vara utförlig. Information du inte kan förstå betydelsen av ignorerar du. "  
    #Create a json struct for previous messages and the current message
    client = AnthropicVertex(region=loc, project_id="sunlit-inn-417922")
    try:
        message = client.messages.create(
        max_tokens=1500,
        model=model,
        messages = [{"content": ("Skapa en tidslinje för denna text. Svara på formatet {time :\"åå-mm-dd hh:mm\" , event: \"händelsebeskrivning\"}. Här är materialet du ska behandla  :" + input), "role": "user"}],
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
for elem in splits[:10]:
    #Send in 5 splits at a time
    timelines.append(summarise(elem.page_content))
    totind += 1
    print("totind: ", totind)
megastring = ""
struct = []
for elem in timelines:
    #Drop the first two lines in elem bc these contain garbage from the prompt
    #TODO: Change this to a more robust solution, e.g. by checking if lines are on desired format
    elem = "\n".join(elem.split("\n")[2:])
    #print("TIMELINE: ")
    #print(elem)
    megastring += elem
    elem = elem.split("\n")
    for line in elem:
        #print("LINE: ", line)
        #Check that line starts with {time, and is not empty, else ignore
        if len(line) > 0 and "time" in line and "event" in line:
            #Events are on the form {time: "2022-03-01 12:00", event: "Event description"}, {time : "22-06-01", event : "DNA-analys slutredovisad."}, extract these
            #Find index of first and second ", and extract the strings between them as time
            ttime = line[line.find("\"")+1:line.find("\"", line.find("\"")+1)]
            #Find index of third ", and extract the substring after this as event
            event = line[line.find("event")+8:]
            #Remove trailing ", and }
            event = event[:event.find("}")]
            #Remove the first and last char 
            event = event[1:-1]
            #print("TIME: ", ttime)
            #print("EVENT: ", event)
            #Convert to date object
            struct.append({"time": ttime, "event": event})
            
from dateutil import parser
from dateutil import tz
#print("STRUCT: ", struct)
for elem in struct:
    #Remove the first char
    #Time is on the form "2022-03-01 12:00", or "22-06-01", convert to datetime object
    elem["time"] = elem["time"].replace(" ", "T")
    try:
        elem["time"] = parser.parse(elem["time"])
    except:
        print("PROBLEMATIC TIME:", elem["time"])
        print("Content", elem["event"])
        print("Length: ", len(elem["time"]))
        elem["time"] = parser.parse("1999/01/01 00:00")
    # try:
        # if len(elem["time"]) == 16:
        #     elem["time"] = time.strptime(elem["time"], "%Y-%m-%d %H:%M")
        # elif(len(elem["time"]) == 10):
        #     elem["time"] = time.strptime(elem["time"], "%Y-%m-%d")
        # #Handle if only year and month is given
        # elif(len(elem["time"]) == 7):
        #     elem["time"] = time.strptime(elem["time"], "%y-%m")
        # else:
        #     elem["time"] = time.strptime(elem["time"], "%Y")
    # except:
    #     print("PROBLEMATIC TIME: ", elem["time"])
    #     print("Content", elem["event"])
    #     print("Length: ", len(elem["time"]))
    #     elem["time"] = time.strptime("1999-01-01", "%Y-%m-%d")
#Order all events by time
struct = sorted(struct, key = lambda x: x["time"].timestamp())
for elem in struct:
    #Print the time as a string
    print( elem["time"])
    print(elem["event"])
# print("STRUCT: ", struct)
#Summarise megastring
#Note: Denhär fucking suger län
# print("MEGASTRING: "+ make_summary(megastring))



