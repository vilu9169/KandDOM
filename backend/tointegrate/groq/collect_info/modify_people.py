import os

from groq import Groq

from dotenv import load_dotenv

from collection_tools import tools

from time import time

import json

from util import print_tool_call

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

instructions = """
Du är en assistent på ett arkiv som håller information om personer, du får meddelanden som ger ny information
om personen och din uppgift är att få med den nya information, utan att ta bort information, varken från
den nya eller gamla informationen. Ge din nya version av arkivinformationen. 
All information ska vara på svenska.
"""


ny_info = ""

gammal_info = ""

text = "Ny information: \n"+ny_info+"Tidigare känd information: \n"+gammal_info

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