#A summarizer utilising claud
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import TextLoader
from langchain_google_vertexai import VertexAIEmbeddings
from dateutil import parser
from vertexai.generative_models import GenerativeModel, Part, FinishReason
import vertexai.preview.generative_models as generative_models
from time import time
from time import sleep
import vertexai
from pinecone import Pinecone
from groq import Groq
import json
tools = {
    "timelinemaker": {
        "type": "function",
        "function": {
            "name": "skapa_händelse",
            "description": "Använd för att spara information, tid och sidreferenser till en händelse. Skriv in datum och tid för händelsen, sidor där informationen finns och information om händelsen. Var noga med att skriva på svenska.",
            "parameters": {
                "type": "object",
                "properties": {
                    "time": {
                        "type": "string",
                        "description": "Datum och tid då händelsen inträffade. Skall endast vara en tid per händelse. Tider ska anges på formatet DD/MM/YY HH:MM",
                    },
                    "pages": {
                        "type": "string",
                        "description": "Sidnummer till sidorna där information om händelsen finns.",
                    },
                    "information": {
                        "type": "string",
                        "description": "Information om händelsen.",
                    },
                },
                "required": ["time","pages","information"],
            },
        },
    },
}


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
vectorstore = PineconeVectorStore(  
    index, embeddings  
)  

def summarise_gemeni_par(input, index, res):

    cont = "Du är en LLM som hämtar och dokumenterar händelser, när de skedde och på vilka sidor det finns information om dem. Alla dina svar måste vara på svenska. Dokumentera alla händelser du identifierar i texten med en beskrivning av händelsen och datum samt tidpunkten när den skede. Tidpunkter ska vara på formatet Tider ska anges på formen DD/MM/YY HH:MM. Var utförlig i händelsebeskrivningarna och tillse att de är på svenska. Du måste alltid inkludera vilka sidor du hittade informationen. Här är materialet du ska behandla  :" + input 
    generation_config = {
    "max_output_tokens": 4400,
    "temperature": 0.1,
    "top_p": 1,
    }

    safety_settings = {
        generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
        generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
        generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
        generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
    }
    vertexai.init(project="sunlit-inn-417922", location="us-central1")
    model = GenerativeModel("gemini-1.5-pro-preview-0409")
    #model = GenerativeModel("gemini-1.0-pro")
    
    while True:
        try:
            response = model.generate_content(
                [cont],
                generation_config=generation_config,
                safety_settings=safety_settings,
            )
            #print("Response: ", response)

            try :
                res[index]= response.text
                return
            except Exception as e:
                print("Error likely due to block_reason for: ", e)
                return
        except Exception as e:
            print("Error: ", e)
            #Sleep for 20 seconds
            sleep(20)
     
#Handles parsing a split using functions in LLAMA3 hosted on Groq
def handlesplit(split, retvals, i):
    if(len(split) == 0):
        retvals[i] = []
        return
    instructions = """
    Du är en funktionsanropande LLM.
    Ditt jobb är att skapa händelser utifrån en text. Läs texten och skapa händelser med hjälp ett verktyg som sparar en händelsebeskrivning tillsammans med händelsens tid och vilka sidor man kan läsa om händelsen på . Det ska vara exakt en tid per händelse.
    Du sak använda verktyget \"skapa_händelse\" och ange tider på formen DD/MM/YY HH:MM. Det är absolut förbjudet att inte ange en tid på detta format.
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
                temperature=0.1,
            )
            break
        except Exception as e:
            print(e)
            print("Error during split handling")
            #Sleep for 20 seconds
            sleep(20)
            continue
    ret = []
    try:
        for tool_call in events.choices[0].message.tool_calls:
            args = json.loads(tool_call.function.arguments)
            #Add to dict
            try :
                ret.append({"time": parser.parse(args["time"]),"pages": args["pages"] , "information": args["information"]})
            except Exception as e:
                #Append time anyways
                ret.append({"time": args["time"],"pages": args["pages"] , "information": args["information"]})
        retvals[i] = ret
        pass
    except Exception as e:
        print(e)
        print("No tool calls")
        pass
    
def bettersort(theevents):
    if(type(theevents["time"]) == str):
        return 0
    else:
        return theevents["time"].timestamp()
def analyzefromstr(input):
    from langchain.docstore.document import Document

    doc =  Document(page_content=input, metadata={"source": "local"})
    #Load inputstring as a document
    # Split documents
    maxclaudin = 50000
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = maxclaudin, chunk_overlap = 0)
    splits = text_splitter.split_documents([doc])
    print("number of splits: ", len(splits))
    timelines = []
    index = 0
    import threading
    threads = []
    for i in range(len(splits)):
        timelines.append([])
    print("Timeline length: ", len(timelines))
    #Summarise parts of the text
    for elem in splits:
        t = threading.Thread(target=summarise_gemeni_par, args=(elem.page_content, index, timelines))
        index += 1
        threads.append(t)
        t.start()

    for i in range(len(threads)):
        threads[i].join()
    #Process summaries with lama
    struct = []
    threads = []
    retvals = []
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
    struct = sorted(struct, key = lambda x: bettersort(x))
    for elem in struct:
        #Print the time as a string
        elem["time"] = str(elem["time"])
    merged = ""
    # for elem in struct:
    #     merged += "{time : \"" + elem["time"] + "\" pages : " + elem["pages"] + "\", event : \"" + elem["information"] + "\"}\n"
    # #Split data again and clean it
    # # res = []
    # # newspltis = 10000
    # # splits = [merged[i:i+newspltis] for i in range(0, len(merged), newspltis)]
    # # for i in range(len(splits)):
    # #     res+=cleandates(splits[i])
    # #Order all events by time
    # #srted = sorted(res, key = lambda x: bettersort(x))

    # #Parse as desired
    # for elem in srted:
    #     elem["time"] = str(elem["time"].strftime("%d/%m/%Y %H:%M"))
    for elem in struct:
        try:
            elem["time"] = parser.parse(elem["time"])
            elem["time"] = str(elem["time"].strftime("%d/%m/%Y %H:%M"))
        except Exception as e:
            print("Error parsing time: ", e)
    return struct

# timerstart = time()
# with open("schizzomord.txt", "r", encoding="utf-8") as file:
#     filecontents = file.read()
# res = analyzefromstr(filecontents)
# print("Time taken: ", time()-timerstart)
# for elem in res:
#     print(elem)
#     print("\n\n")