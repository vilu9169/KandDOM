from groq import Groq

#from dotenv import load_dotenv

from collection_tools import tools

from time import time
from time import sleep
import json

def handlesplit(split, retvals, i):
    while True:
        try:
            events = client.chat.completions.create(
                messages=[{
                    "role": "system",
                    "content": "Summera händelserna i texten och inkludera när de skede. Du måste få med alla händelser. Svara på svenska. ",
                    
                },
                {
                    "role": "user",
                    "content": split,
                }],
                model="llama3-70b-8192",
                temperature=0.1,
            )
            break
        except Exception as e:
            print(e)
            print("Error working with model")
            #Sleep for 20 seconds
            sleep(20)
            continue
    split = str(events.choices[0].message.content)
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
                print("Could not parse time")
                ret.append({"time": args["time"], "information": args["information"]})
        retvals[i] = ret
        pass
    except Exception as e:
        print(e)
        print("No tool calls")
        pass
        


client = Groq(
    api_key="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",
)

instructions = """
Du är en funktionsanropande LLM.
Ditt jobb är att skapa händelser utifrån en text. Läs texten och skapa händelser med hjälp ett verktyg som sparar en händelsebeskrivning tillsammans med händelsens tid. Det ska vara exakt en tid per händelse.
Svara på svenska.
VIKTIGT: Använd ett av verktygen per händelse.
"""
# Get text from "schizzomord.txt"
text = open("Mord2008.txt", "r").read()
#Split the text into sections of 10000 characters
splitsize = 10000
splits = [text[i:i+splitsize] for i in range(0, len(text), splitsize)]
ttime = time()
# splits = [text]
from dateutil import parser
import threading

threads = []
retvals = []
#Add splits number of dicts to retvals 
for i in range(len(splits)):
    retvals.append([])
# Create and start threads
for i in range(len(splits)):
    t = threading.Thread(target=handlesplit, args=(splits[i], retvals, i))
    threads.append(t)
    t.start()

# Wait for all threads to finish
for thread in threads:
    thread.join()

#merge all the lists in retvals
merge = []

for ret in retvals:
    merge += ret
retvals = merge


print("Time: ", time()-ttime)
def compfun(x):
    try:
        return x["time"].timestamp()
    except:
        return 0
#Sort dict on keys, i.e. time. If parsing fails the time will be set to the epoch
retvals = sorted(retvals, key = lambda x: compfun(x))
#Convert all the times to strings
for event in retvals:
    event["time"] = event["time"].strftime("%Y-%m-%d %H:%M")

print(retvals)
