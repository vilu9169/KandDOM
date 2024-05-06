#A summarizer utilising claud
from langchain_google_vertexai import VertexAIEmbeddings
from dateutil import parser
from vertexai.generative_models import GenerativeModel, Part, FinishReason
import vertexai.preview.generative_models as generative_models
from time import sleep
import vertexai
from pinecone import Pinecone
from groq import Groq
from anthropic import AnthropicVertex
import json
from vertexai.preview.generative_models import (
    HarmCategory, 
    HarmBlockThreshold )
from google.cloud.aiplatform_v1beta1.types.content import SafetySetting
tools = {
    "timelinemaker": {
        "type": "function",
        "function": {
            "name": "skapa_händelse",
            "description": "Använd för att spara information, tid och sidreferenser till en händelse från ett visst dokument. Skriv in datum och tid för händelsen, sidor där informationen finns och information om händelsen. Var noga med att skriva på svenska.",
            "parameters": {
                "type": "object",
                "properties": {
                    "time": {
                        "type": "string",
                        "description": "Datum och tid då händelsen inträffade. Skall endast vara en tid per händelse. Tider kan vara på formatet år-månad-dag eller dag-månad år, du måste avgöra vilket utifrån kontexten. Tider måste alltid sparas på formatet DD/MM/YY HH:MM.",
                    },
                    "pages": {
                        # "type": "array",
                        # "items": {
                        #     "type": "int"
                        # },
                        "type": "string",
                        "description": "Sidnummer till där information om händelsen finns. Varje sidnummer skall bara förekomma en gång.",
                    },
                    "information": {
                        "type": "string",
                        "description": "Information om händelsen.",
                    },
                    "document": {
                        "type": "string",
                        "description": "Namnet på dokumentet som händelsen hämtades ifrån.",
                    }
                },
                "required": ["time","pages","information", "document"],
            },
        },
    },
}




groqalts = ["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", "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","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","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"]
groqind = 0


pc = Pinecone(api_key = "2e669c83-1a4f-4f19-a06a-42aaf6ea7e06")
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

#Summarise the content in some documents
def summarise_claud(input, index, res):
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
    # context = "Skapa en tidslinje baserad på följande dokument. Använd bara information från detta dokument i dina svar och upprepa dig inte. Dethär är en sammanfattning av vad som skett "+ sammanf  
    context = """Du är en LLM som hämtar och dokumenterar händelser, när de skedde och på vilka sidor det finns information om dem.
    Alla dina svar måste vara på svenska. Dokumentera alla händelser du identifierar i texten med en beskrivning av händelsen och datum samt tidpunkten när den skede.
    Tidpunkter ska vara på formatet DD/MM/YY HH:MM. Var utförlig i händelsebeskrivningarna och tillse att de är på svenska. Du måste alltid inkludera vilka sidor du hittade informationen, sidnummer finns efter \"pagestart page\" och \"pageend page\".
    Namnet på dokumentet finns efter texten \"in document\" och ska finnas med. Här är materialet du ska behandla  :""" + input 
    #Create a json struct for previous messages and the current message
    client = AnthropicVertex(region=loc, project_id="sunlit-inn-417922")
    while True:
        try:
            message = client.messages.create(
            model=model,
            messages = [{"content": ("Dokumentera alla händelser du identifierar i texten och inkludera tidpunkten när de sker. Alla relevanta händelser ska dokumenteras. Alla svar skall vara på svenska. Här är materialet du ska behandla  :" + input), "role": "user"}],
            system = context,
            )
            res[index] =  message.content[0].text
        except Exception as e:
            print("Error: ", e)
            optind+=1
            if(optind==len(options)):
                optind = 0
            loc = options[optind]

def summarise_gemeni_par(input, index, res):
    cont = """Du är en LLM som hämtar och dokumenterar händelser, när de skedde och på vilka sidor det finns information om dem.
    Alla dina svar måste vara på svenska. Dokumentera alla händelser du identifierar i texten med en beskrivning av händelsen och datum samt tidpunkten när den skede.
    Tidpunkter ska vara på formatet DD/MM/YY HH:MM. Var utförlig i händelsebeskrivningarna och tillse att de är på svenska. Du måste alltid inkludera vilka sidor du hittade informationen, korrekt sidnummer finns efter \"pagestart page\" och \"pageend page\". Andra sidnummer ska ignoreras.
    Namnet på dokumentet finns efter texten \"in document\" och ska finnas med. Här är materialet du ska behandla  :""" + input 
    generation_config = {
    #"max_output_tokens": 4400,
    "temperature": 0, # 0.1,
    "top_p": 1,
    }

    safety_settings = {
        generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_NONE,
        generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_NONE ,
        generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_NONE ,
        generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_NONE ,
    }
    # safety_settings = [
    #  SafetySetting(
    #      category=HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
    #      threshold=HarmBlockThreshold.BLOCK_ONLY_HIGH,
    #  ),
    #  SafetySetting(
    #      category=HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
    #      threshold=HarmBlockThreshold.BLOCK_ONLY_HIGH,
    #  ),
    #  SafetySetting(
    #      category=HarmCategory.HARM_CATEGORY_HATE_SPEECH,
    #      threshold=HarmBlockThreshold.BLOCK_ONLY_HIGH,
    #  ),
    #  SafetySetting(
    #      category=HarmCategory.HARM_CATEGORY_HARASSMENT,
    #      threshold=HarmBlockThreshold.BLOCK_ONLY_HIGH,
    #  ),
    # ]
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
                print("Response: ", response)
                print("Error likely due to block_reason for: ", e)
                return
        except Exception as e:
            print("Error: ", e)
            #Sleep for 20 seconds
            sleep(20)
     
#Handles parsing a split using functions in LLAMA3 hosted on Groq
def handlesplit(split, retvals, i):
    global groqind, groqalts
    gind = groqind
    galts = groqalts
    client = Groq(
    api_key=galts[gind],
    )
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
                #temperature=0.1,
            )
            break
        except Exception as e:
            print(e)
            print("Error during split handling")
            #Switch to next key
            gind += 1
            if(gind == len(galts)):
                gind = 0
            client = Groq(api_key=galts[gind])
            continue
    ret = []
    try:
        for tool_call in events.choices[0].message.tool_calls:
            args = json.loads(tool_call.function.arguments)
            #Add to dict
            try :
                ret.append({"title": parser.parse(args["time"], dayfirst=True),"pages": args["pages"] , "cardTitle": args["information"],"document": args["document"]})
            except Exception as e:
                #Append time anyways
                ret.append({"title": args["time"],"pages": args["pages"] , "cardTitle": args["information"], "document": args["document"]})
        retvals[i] = ret
        pass
    except Exception as e:
        print(e)
        print("No tool calls")
        pass
    
def bettersort(theevents):
    if(type(theevents["title"]) == str):
        return 0
    else:
        return theevents["title"].timestamp()

def analyzefromstr(input):
    from langchain.docstore.document import Document

    doc =  Document(page_content=input, metadata={"source": "local"})
    #Load inputstring as a document
    # Split documents
    maxclaudin = 20000
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
        # t = threading.Thread(target=summarise_claud, args=(elem.page_content, index, timelines))
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

    struct = sorted(struct, key = lambda x: bettersort(x))
    # for elem in struct:
    #     try:
    #         elem["title"] = str(elem["title"].strftime("%d/%m/%Y %H:%M"))
    #     except Exception as e:
    #         print("Error parsing time: ", e)
    return struct

# timerstart = time()
# with open("schizzomord.txt", "r", encoding="utf-8") as file:
#     filecontents = file.read()
# res = analyzefromstr(filecontents)
# print("Time taken: ", time()-timerstart)
# for elem in res:
#     print(elem)
#     print("\n\n")