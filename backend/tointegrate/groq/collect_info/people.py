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
Ditt jobb är spara information om personer. Du tar emot en lista med kända personer samt en sammanställning
av ny information. Om sammanställningen innehåller information om en person som inte ingår i listan med kända
personer ska du lägga till den personen samt all information om personen med hjälp av ett verktyg.
Om sammanställningen innehåller information om en person som redan finns i listan med kända personer ska du 
istället använda ett verktyg som lägger till ny information om personen. Tänkt på att inkludera all information 
från sammanställningen. All information ska vara på svenska.

VIKTIGT: Använd ett av verktygen per person som nämns i sammanställningen.
"""


lista = """
Kända personer:\n
Rikard Ahlkvist, IT-student på Uppsala Universitet, riktigt jobbig att ha att göra med,\n
CJ, lite av en kung,\n

Ny information:\n
"""

file = ""

text = """Björn Westerlund är en person som är väldigt jobbig att ha att göra med. Han är en IT-student på 
Uppsala Universitet. CJ gillar inte Björn. Men CJ gillar Calle Back eftersom han är lite av en kung.
Calle studerar också i uppsala. Han är även mycket bättre än Björn på att programmera. Björn kan inte läsa 
eller skriva.
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
    #tools = [tools["ny_person"]],
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
            "content": lista+extracted,
        }
    ],
    tools = [tools["ny_person"], tools["ny_info"]],
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