import os
from groq import Groq
from dotenv import load_dotenv
from time import time
import json
from vertexai.generative_models import GenerativeModel, GenerationConfig

from collection_tools import tools
from util import print_tool_call, gemini_unfiltered


instructions = """
Ditt jobb är att sammanställa information om personer från en text. Sammanställningen sak ha tre delar.\n
1. Sammanfatta först vad texten handlar om i grova drag. \n
2. Sammanställ all information om de olika personerna, gör en rubrik för varje person och gör sedan en punktlista\n
med information om personerna, var nogrann med att inkludera allt som står om personerna.
3. Sammanställ de relationer och kopplingar som nämns mellan personerna. Gör detta under en och samma rubrik.
En koppling ska alltid vara mellan två personer och ska vara tydligt beskriven. \n
4. Sammanställ grupperingar av personer som nämns i texten om de förekommer, t. ex. en familj, företag, organisation etc. . Gör detta under en och samma rubrik. \n
Det är viktigt att du alltid svarar på svenska.
"""

tool_instructions = """
Ditt jobb är spara information om personer. Du får en sammanställning av informationen som samlats in. Till'
din hjälp har du två verktyg. Det ena verktyget används för att lägga till information om en person. 
Det andra vertyget registrerar information om relationen mellan två personer.
Informationen som skickas in ska alltid vara på svenska. Om texten är på engelska, översätt det till svenska. \n

Om något är otydligt kan du använda ett verktyg för att ställa frågor om orginalmaterialet. \n

VIKTIGT: Använd verktyget en gång per person som nämns i sammanställnignen och registrera all information om
personerna. 
"""



file_path = "KandDOM/backend/tointegrate/Mord2008.txt"

text = """Björn Westerlund är en person som är väldigt jobbig att ha att göra med. Han är en IT-student på 
Uppsala Universitet. CJ gillar inte Björn. Men CJ gillar Calle Back eftersom han är lite av en kung.
Calle studerar också i uppsala. Han är även mycket bättre än Björn på att programmera. Björn kan inte läsa 
eller skriva. Björns kusin tycker också att han är jobbig. Han är glad att han inte pluggar i Uppsala så att 
han slipper träffa Björn. Den 17:e Maj rånade Björn en spritaffär i Oslo tillsammans med Rikard.
"""
with open(file_path, "r") as file:
    text = file.read()


def summarize_people_groq(text):
    load_dotenv()
    client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)
    start = time()
    extract_people_info = client.chat.completions.create(
        temperature=0.0,
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

    print("done in", time() - start, "seconds")

    extracted = ""
    try:
        extracted = extract_people_info.choices[0].message.content
        print(extracted)
        return extracted
    except:
        print("no message")

def summarize_people_gemini(text):
    start = time()
    model = GenerativeModel("gemini-1.0-pro", system_instruction=[instructions], safety_settings=gemini_unfiltered)
    chat = model.start_chat()
    summary = chat.send_message(text).candidates[0].content.text
    print(summary)
    print("done in", time() - start, "seconds")
    return summary

def use_tools_on_summary(summary):
    load_dotenv()
    client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)
    start = time()
    log_people_info = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": tool_instructions,
            },
            {
                "role": "user",
                "content": summary,
            }
        ],
        tools = [tools["ny_information_om_person"], tools["ny_info_relation"], tools["ny_gruppering"]],
        model="llama3-70b-8192",
    )

    try:
        print("\n")
        for tool_call in log_people_info.choices[0].message.tool_calls:
            print_tool_call(tool_call)
        return log_people_info.choices[0].message.tool_calls
    except Exception as e:
        print(e)
        print("No tool calls")


    print("done in", time() - start, "seconds")


    