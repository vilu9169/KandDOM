#A summarizer utilising claud
from langchain.text_splitter import  RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import TextLoader
from anthropic import AnthropicVertex
from langchain_google_vertexai import VertexAIEmbeddings
from collection_tools import tools
from dateutil import parser

from time import time
from time import sleep

from pinecone import Pinecone
from groq import Groq
import json

client = Groq(
    api_key="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",
)
pc = Pinecone(api_key="2e669c83-1a4f-4f19-a06a-42aaf6ea7e06")
index_name = "gbgmordforsok"
index = pc.Index(index_name)  

loc_sonnet = "europe-west4"
loc_haiku = "us-central1"
model_haiku = "claude-3-haiku@20240307"
model_sonnet = "claude-3-sonnet@20240229"
optind_sonnet = 0
optind_haiku = 0

#Sonnet below
options_sonnet = ["us-central1", "asia-southeast1"]
options_haiku = ["us-central1", "europe-west4"]
loc_sonnet = options_sonnet[optind_sonnet]
loc_haiku = options_haiku[optind_haiku]

embeddings = VertexAIEmbeddings(model_name="textembedding-gecko-multilingual@001")

from langchain_pinecone import PineconeVectorStore  
#Load document text from file
# with open(FIlE_PATH, "r", encoding="utf-8") as f:
#     text_field = f.read()
vectorstore = PineconeVectorStore(  
    index, embeddings  
)  

def sammanfattning():
    # global loc_haiku, optind_haiku, options_haiku, model_haiku
    # loc = loc_haiku
    # optind = optind_haiku
    # options = options_haiku
    # model = model_haiku
    
    global loc_sonnet, optind_sonnet, options_sonnet, model_sonnet
    loc = loc_sonnet
    optind = optind_sonnet
    options = options_sonnet
    model = model_sonnet
    
    sammanf = ""
    index = 0
    prepend = ""
    append = ""
    
    for rag in vectorstore.as_retriever(search_type="mmr", search_kwargs = ({"k" : 40, })).invoke( "Identifiera nyckelhändelserna i texten. Vilka är de centrala händelserna i brottet? Vad har skett och vilka är huvudpersonerna?"):
        if index < 10:
            prepend += rag.page_content
        elif index >10 and index < 20:
            append = rag.page_content + append
        else:
            prepend += rag.page_content
        index += 1
    sammanf = prepend + append
    #Ask Haiku to summarise the text
    client = AnthropicVertex(region=loc, project_id="sunlit-inn-417922")
    while True:
        try:
            message = client.messages.create(
            max_tokens=1500,
            model=model,
            messages = [{"content": ("Summera innehållet i detta material" + sammanf), "role": "user"}],
            )
            return message.content[0].text
        except Exception as e:
            print("Error: ", e)
            optind+=1
            if(optind==len(options)):
                optind = 0
            loc = options[optind]

sammanf = sammanfattning() 


#Summarise the content in some documents
def summarise(input):
    global loc_haiku, optind_haiku, options_haiku, model_haiku
    global loc_sonnet, optind_sonnet, options_sonnet, model_sonnet
    # model = model_haiku
    # loc = loc_haiku
    # optind = optind_haiku
    # options = options_haiku
    model = model_sonnet
    loc = loc_sonnet
    optind = optind_sonnet
    options = options_sonnet
    print("loc: ", loc)
    # Set the endpoint URL
    context = "Skapa en tidslinje baserad på följande dokument. Använd bara information från detta dokument i dina svar och upprepa dig inte. Dethär är en sammanfattning av vad som skett "+ sammanf  
    #Create a json struct for previous messages and the current message
    client = AnthropicVertex(region=loc, project_id="sunlit-inn-417922")
    while True:
        try:
            message = client.messages.create(
            max_tokens=1500,
            model=model,
            messages = [{"content": ("Dokumentera alla händelser du identifierar i texten och inkludera tidpunkten när de sker. Alla relevanta händelser ska dokumenteras. Alla svar skall vara på svenska. Här är materialet du ska behandla  :" + input), "role": "user"}],
            system = context,
            )
            return message.content[0].text
        except Exception as e:
            print("Error: ", e)
            optind+=1
            if(optind==len(options)):
                optind = 0
            loc = options[optind]
            
   
#Handles parsing a split using functions in LLAMA3 hosted on Groq
def handlesplit(split, retvals, i):
    instructions = """
    Du är en funktionsanropande LLM.
    Ditt jobb är att skapa händelser utifrån en text. Läs texten och skapa händelser med hjälp ett verktyg som sparar en händelsebeskrivning tillsammans med händelsens tid. Det ska vara exakt en tid per händelse.
    Svara på svenska. Du sak använda verktyget \"skapa_händelse\". Saknas en angiven tid för en händelse ska tiden sättas till 00:00:00. Saknas datum ignorerar du händelsen.
    VIKTIGT: Använd ett av verktygen per händelse.
    """
    while True:
        try:
            events = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": instructions,
                    },
                    {
                        "role": "user",
                        "content": split,
                    }
                ],
                tools = [tools["timelinemaker"]],
                model="llama3-70b-8192",
                temperature=0.0,
            )
            break
        except Exception as e:
            print(e)
            print("Error working with model")
            #Sleep for 20 seconds
            sleep(20)
            continue
    ret = []
    try:
        for tool_call in events.choices[0].message.tool_calls:
            args = json.loads(tool_call.function.arguments)
            #Add to dict
            try :
                ret.append({"time": parser.parse(args["time"]), "information": args["information"]})
            except Exception as e:
                print(e)
                print("Could not parse time in handlesplit")
                # ret.append({"time": args["time"], "information": args["information"]})
        retvals[i] = ret
        pass
    except Exception as e:
        print(e)
        print("No tool calls")
        pass


#Cleans the dates and times by merging and removing duplicates
def cleandates(dates):
    #Merge dates
    instructions = """
    Du är en funktionsanropande LLM.
    Du har fått in en rörig samling händelser där det kan finnas duppletter av samma händelse vid samma eller olika tid.
    Om dupletter förekommer ska de tas bort. Om händelserna skiljer sig åt men skett vid samma tid ska de slås ihop till en händelse.
    Händelser som sker 00:00:00 är troligen relateraade till dagen i helhet så förekommer en mer specifik tid för händelsen ska den
    mer specifika tiden användas och 00:00:00 tas bort. 
    Svara på svenska.
    VIKTIGT: Använd ett av verktygen per händelse.
    """
    
    while True:
        try:
            events = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": instructions,
                    },
                    {
                        "role": "user",
                        "content": dates,
                    }
                ],
                tools = [tools["timelinemaker"]],
                model="llama3-70b-8192",
                temperature=0.0,
            )
            break
        except Exception as e:
            print(e)
            print("Error working with model")
            #Sleep for 20 seconds
            sleep(20)
            continue
    ret = []
    try:
        for tool_call in events.choices[0].message.tool_calls:
            args = json.loads(tool_call.function.arguments)
            #Add to dict
            try :
                ret.append({"time": parser.parse(args["time"]), "information": args["information"]})
            except Exception as e:
                print(e)
                print("Could not parse time in cleandates")
                #print the information
                print(args["information"])
                #Error occurs when time comes on format 2022-02-25 --:--
                #Extract date and use 00:00 as time
                # time = args["time"].split(" ")[0]
                # time += " 00:00"
                # ret.append({"time": parser.parse(time), "information": args["information"]})
        return ret
    except Exception as e:
        print(e)
        print("No tool calls")
        pass
    

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
#Summarise the texts
for elem in splits[:3]:
    #Send in 5 splits at a time
    summary = summarise(elem.page_content)
    totind += 1
    print("totind: ", totind)
    timelines.append(summary)

#Process summaries with lama
struct = []
#Create a thread for each timeline
threads = []
retvals = []
import threading
for i in range(len(timelines)):
    retvals.append([])
    t = threading.Thread(target=handlesplit, args=(timelines[i], retvals, i))
    threads.append(t)
    t.start()

for i in range(len(timelines)):
    threads[i].join()

struct = []
for elem in retvals:
    struct += elem

#Order all events by time
#Todo rework to only drop events without time in the second iteration and keep for the first
#Use a better sortfunction to accomplish this instead of the current one
struct = sorted(struct, key = lambda x: x["time"].timestamp())

for elem in struct:
    #Print the time as a string
    elem["time"] = str(elem["time"])
merged = ""
for elem in struct:
    merged += "{time : \"" + elem["time"] + "\", event : \"" + elem["information"] + "\"}\n"
#Print the data before the clean
print("Before clean: ", merged)


#Clean the data
res = cleandates(merged)

#Order all events by time
res = sorted(res, key = lambda x: x["time"].timestamp())
#Convert all the times to strings and print
for event in res:
    event["time"] = str(event["time"])
    print("{time : \"" + event["time"] + "\", information : \"" + event["information"] + "\"}")
    print("\n")