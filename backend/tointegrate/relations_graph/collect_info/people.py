import os
from groq import Groq
from dotenv import load_dotenv
from time import time
import json
from vertexai.generative_models import GenerativeModel, GenerationConfig

#from collection_tools import tools
from tool_tests.openai_tools import tools
from util import print_tool_call, gemini_unfiltered
from get_predictions import get_claude_prediction_string, get_openai_prediction


from openai import OpenAI


summary_instructions = """
Ditt jobb är att sammanställa information om personer från en text. Sammanställningen sak ha tre delar.\n
1. Sammanfatta först vad texten handlar om i grova drag. \n
2. Sammanställ all information om de olika personerna, gör en rubrik för varje person och gör sedan en punktlista\n
med information om personerna, var nogrann med att inkludera allt som står om personerna.
3. Sammanställ de relationer och kopplingar som nämns mellan personerna. Gör detta under en och samma rubrik.
En koppling ska alltid vara mellan två personer och ska vara tydligt beskriven. \n
4. Sammanställ grupperingar av personer som nämns i texten om de förekommer, t. ex. en familj, företag, organisation etc. . Gör detta under en och samma rubrik. \n
Det är viktigt att du alltid svarar på svenska. Skriv all information med fullständiga meningar och ange på vilken sida i texten du hittade informationen.
"""

tool_instructions = """
Ditt jobb är spara information om personer. Du får en sammanställning av informationen som samlats in. Till
din hjälp har du tre verktyg. Det första verktyget används för att lägga till information om en person. 
Det andra vertyget registrerar information om relationen mellan två personer.
Det tredje verktyget används för att registrera information om en gruppering av personer, t. ex. en familj, företag, organisation etc.

Använd verktygen flera gånger, en gång per person, relation eller gruppering.
"""

tool_instructions2 = """
Ditt jobb är spara information om personer och relationer. Du får en sammanställning av informationen som samlats in. Du ska
sedan spara informationen genom att använda verktyg där du anger namn och information om alla personer och relationer,
ordnade i listor.
"""


relations_instructions = """
Ditt jobb är att spara information om relationer mellan olika personer i text, varje relation består av två personer samt information om hur de är kopplade till varandra.
Använd verktyget flera gånger, en gång per relation.
"""




file_path = "KandDOM/backend/tointegrate/Mord2008.txt"

with open(file_path, "r") as file:
    text = file.read()


def summarize_people(text):
    start = time()
    summary = get_claude_prediction_string(text, summary_instructions, use_vertex=True)
    print(summary)
    print("done in", time() - start, "seconds")
    return summary



def use_tools_on_summary(summary):
    load_dotenv()
    client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)
    client = OpenAI()
    start = time()
    log_people_info = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": tool_instructions2,
                #"content" : relations_instructions,
            },
            {
                "role": "user",
                "content": summary,
            }
        ],
        tools = [
                 tools["spara_information_om_personer"],
                 tools["spara_information_om_relationer"], 
                 #tools["ny_information_om_gruppering"],
        ],
        #model="gpt-4-turbo-2024-04-09",
        #model="gpt-3.5-turbo-0125"
        model="gpt-4o",
    )

    try:
        print("\n")
        return log_people_info.choices[0].message.tool_calls
    except Exception as e:
        print(e)
        print("No tool calls")


    print("done in", time() - start, "seconds")


    