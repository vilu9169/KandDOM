import os

from groq import Groq

from dotenv import load_dotenv

from collection_tools import tools

from time import time

import json


load_dotenv()

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

instructions = """
Ditt jobb är att sammanställa information om personer från en text. Läs texten nedan och sammanställ och 
separera den information som står om de olika personerna. Svara på svenska.
"""

tool_instructions = """
Ditt jobb är spara information om personer. Du får en sammanställning av informationen som samlats in. Du ska
spara informationen om personerna genom att använda verktyget "lägg_till_info". 

VIKTIGT: Använd verktyget en gång per person som nämns i sammanställnignen och registrera all information om
personerna.
"""


file = ""

text = """Björn Westerlund är en person som är väldigt jobbig att ha att göra med. Han är en IT-student på 
Uppsala Universitet. CJ gillar inte Björn. Men CJ gillar Calle Back eftersom han är lite av en kung.
Calle studerar också i uppsala. Han är även mycket bättre än Björn på att programmera. Björn kan inte läsa 
eller skriva. Björns kusin tycker också att han är jobbig. Han är glad att han inte pluggar i Uppsala så att 
han slipper träffa Björn.
"""
# with open("text.txt", "r") as file:
#     text = file.read()



start = time()
extract_people_info = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": instructions,
        },
        {
            "role": "user",
            "content": text,
        }
    ],
    #model="llama2-70b-4096"
    #model="mixtral-8x7b-32768"
    model="llama3-70b-8192",
)


extracted = ""
try:
    extracted = extract_people_info.choices[0].message.content
    print(extracted)
except:
    print("no message")

log_people_info = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": tool_instructions,
        },
        {
            "role": "user",
            "content": extracted,
        }
    ],
    tools = [tools["ny_info"]],
    model="llama3-70b-8192",
)

try:
    for tool_call in log_people_info.choices[0].message.tool_calls:
        args = json.loads(tool_call.function.arguments)
        print(tool_call.function.name+"(namn: '"+args["namn"], 
              "', info: '"+args["information"]+"')")
        print("\n")
except Exception as e:
    print(e)
    print("No tool calls")


print("done in", time() - start, "seconds")

