#A summarizer utilising claud
from langchain.text_splitter import  RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import TextLoader
from anthropic import AnthropicVertex

loc = "europe-west4"
#model = "claude-3-haiku@20240307"
model = "claude-3-sonnet@20240229"
optind = 0
options = ["us-central1", "asia-southeast1"]
#options = ["us-central1", "europe-west4"]
loc = options[optind]

def summarise(input):
    global loc, optind, options
    print("loc: ", loc)
    # Set the endpoint URL
    context = "Skapa en tidslinje baserad på följande dokument. Använd bara information från detta dokument i dina svar och upprepa dig inte. Svara på formatet {time : \"åååå-mm-dd hh:mm\", event : \"händelsebeskrivning\"}. Händelsebeskrivningen ska vara utförlig. Information du inte kan förstå betydelsen av ignorerar du. "  
    #Create a json struct for previous messages and the current message
    client = AnthropicVertex(region=loc, project_id="sunlit-inn-417922")
    try:
        message = client.messages.create(
        max_tokens=1500,
        model=model,
        messages = [{"content": ("Skapa en tidslinje för denna text. Svara på formatet {time :\"åå-mm-dd hh:mm\" , event: \"händelsebeskrivning\"}. Det är strikt förbjudet att svaret innehåller delar som inte är på detta format. Alla svar skall vara på svenska. Materillet kan i vissa fall vara korrupt och i sådant fall ignoreras helt. Här är materialet du ska behandla  :" + input), "role": "user"}],
        system = context,
        )
        return message.content[0].text
    except Exception as e:
        print("Error: ", e)
        optind+=1
        if(optind==len(options)):
            optind = 0
        loc = options[optind]
        return(summarise(input))
   

def make_summary(input):
    global loc, optind, options
    print("loc: ", loc)
    context = "Du får in en tidslinje med händelser med tid och händelsebeskrivning. Du ska nu sammanfatta denna information. Svara på formatet {time :\"åååå-mm-dd hh:mm\" , event: \"händelsebeskrivning\"}. Det är strikt förbjudet att svaret innehåller delar som inte är på detta format. Alla svar skall vara på svenska. "
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
        optind+=1
        if(optind==len(options)):
            optind = 0
        loc = options[optind]
        return(make_summary(input))



#Clean up the data        
def cleaned(olddata):
    print("Olddata = ", olddata)
    #Get unqiue times from all events in olddata
    keys = []
    for event in olddata:
        if event["time"] not in keys:
            keys.append(event["time"])
    newdata = []
    for key in keys:
        #Get all events where time is key
        events = [event for event in olddata if event["time"] == key]
        #Get the first event
        str =""
        #If there are multiple events, concatenate them
        for event in events:
            str += event["event"]
        #Ask claud to summarise the string
        newdata.append({"time": key, "event": str})
    #Convert the newdata to a string
    asstr = ""
    for event in newdata:
        #If time has no hour and minute, only print date
        time = event["time"].strftime("%Y-%m-%d %H:%M")
        print("TIME: ", time)
        asstr += time + ": " + event["event"] + "\n"
    #Ask claud to remove duplicate information from events 
    struct =  make_summary(asstr)
    #Convert the struct to a list of dictionaries
    elem = struct.split("\n")
    struct = []
    for line in elem:
        #print("LINE: ", line)
        #Check that line starts with {time, and is not empty, else ignore
        if len(line) > 0 and "time" in line and "event" in line:
            #Events are on the form {time: "2022-03-01 12:00", event: "Event description"}, {time : "22-06-01", event : "DNA-analys slutredovisad."}, extract these
            #Find index of first and second ", and extract the strings between them as time
            ttime = line[line.find("\"")+1:line.find("\"", line.find("\"")+1)]
            #Find index of third ", and extract the substring after this as event
            print("LINE: ", line)
            event = line[line.find("event: \"") + 8:]
            event = event[:event.find("\"}")]
            print("Event = ", event)
            struct.append({"time": ttime, "event": event})
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
    #Order all events by time
    struct = sorted(struct, key = lambda x: x["time"].timestamp())
    return struct




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
for elem in splits[:2]:
    #Send in 5 splits at a time
    timelines.append(summarise(elem.page_content))
    totind += 1
    print("totind: ", totind)
megastring = ""
struct = []

for elem in timelines:
    #Drop the first two lines in elem bc these contain garbage from the prompt
    #TODO: Change this to a more robust solution, e.g. by checking if lines are on desired format
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
            if(event[0]=="\""):
                event=event[1:]
            if(event[-1]=="\""):
                event=event[:-1]
            #print("TIME: ", ttime)
            #print("EVENT: ", event)
            #Convert to date object
            struct.append({"time": ttime, "event": event})
        
    
            
from dateutil import parser
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
#Order all events by time
struct = sorted(struct, key = lambda x: x["time"].timestamp())


struct = cleaned(struct)
for elem in struct:
    #Print the time as a string
    print( elem["time"])
    print(elem["event"])