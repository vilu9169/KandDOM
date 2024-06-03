from openai_tools import tools
from get_predictions import get_openai_prediction
from dotenv import load_dotenv
from util import print_tool_call


load_dotenv()

text : str

file_path = "KandDOM/fuppar_txt/schizzomord.txt"

with open(file_path, "r") as file:
    text = file.read()

pages = text.split(chr(28))


to_process = pages[0]


text : str

file_path = "KandDOM/fuppar_txt/schizzomord.txt"

with open(file_path, "r") as file:
    text = file.read()



page1_summary = """
Texten är ett förundersökningsprotokoll från polisen i Region Väst, Utredning 2 PO Älvsborg. Det handlar om ett brott som inträffade den 18 februari 2023 klockan 16:10 på Ica City Centrum, Allégatan 21 i Borås. Oliwer Erik Larsson är misstänkt för brott mot lagen om förbud beträffande knivar och andra farliga föremål, grovt brott, samt mord. Lars Nicklas Persson är vittne i ärendet.

Information om personerna:

1. Angela Larsson
   - Målsägande

2. Saga Larsson 
   - Målsägande

3. Loke Larsson
   - Målsägande 

4. Neo Larsson
   - Målsägande

5. Håkan Larsson 
   - Målsägande

6. Oliwer Erik Larsson
   - Misstänkt för brott mot lagen om förbud beträffande knivar och andra farliga föremål, grovt brott, samt mord
   - Personnummer: 20040131-5759
   - Har två undulater som husdjur och har just börjat studera på Borås Yrkeshögskola, inriktning mot bygg och anläggning
   - Har aldrig varit i kontakt med polisen tidigare, har inga tidigare brott i belastningsregistret
   - Vill inte svara på frågor om brottet

7. Lars Nicklas Persson
   - Vittne

Relationer och kopplingar mellan personerna:

Lars Nicklas Persson är vittne i ärendet om brottet som Oliwer Erik Larsson är misstänkt för.

Grupperingar av personer:

Texten nämner fem personer med efternamnet Larsson - Angela Larsson, Saga Larsson, Loke Larsson, Neo Larsson och Håkan Larsson. Detta tyder på att dessa personer troligen tillhör samma familj. Dock finns det inga ytterligare uppgifter som bekräftar detta.
"""


tool_instructions = """
Ditt jobb är spara information om personer. Du får en sammanställning av informationen som samlats in. Till
din hjälp har du tre verktyg. Det första verktyget används för att lägga till information om en person. 
Det andra vertyget registrerar information om relationen mellan två personer.
Det tredje verktyget används för att registrera information om en gruppering av personer, t. ex. en familj, företag, organisation etc.

Använd verktygen flera gånger, en gång per person, relation eller gruppering.
"""
tools = [tools["spara_information_om_personer"], tools["spara_information_om_relationer"], tools["ny_information_om_gruppering"]]



result = get_openai_prediction(page1_summary, tool_instructions, model="gpt-4o-2024-05-13", tools=tools)

#result = get_openai_prediction(page1_summary, tool_instructions, tools=tools)

tool_calls = result.choices[0].message.tool_calls

for tool_call in tool_calls:
    print_tool_call(tool_call)
    print("\n")