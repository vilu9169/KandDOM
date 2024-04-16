import PyPDF2
import vertexai
from vertexai.preview.generative_models import GenerativeModel
from langchain_google_vertexai import ChatVertexAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

from time import time

PROJECT_ID = "robust-summit-417910"
REGION = "us-central1" #"europe-west4"
vertexai.init(project=PROJECT_ID, location=REGION)

pdf_file = "fuppar_ocr/ocr_Uppsala TR B 2613-23 Aktbil 21.pdf"

texts = []

start_page = 0 
no_pages = 10

with open(pdf_file, 'rb') as file:
    reader = PyPDF2.PdfReader(file)

    for page in reader.pages[start_page:start_page+no_pages]:
        text = page.extract_text()
        texts.append(text)

gemini_pro = ChatVertexAI(model_name="gemini-pro", temperature=0, location="us-central1", convert_system_message_to_human=True)



instructions : str = "Det här är textavläsning av en sida från ur en pdf, din uppgift är att avgöra om någon av följade fall stämmer in på texten: " \
"1. Om texten ser ut att komma från ett formulär" \
"2. Om texten ser ut som en intervju" \
"3. Om sidan innehåller lite text totalt, där lite innebär ca 50 ord eller mindre." \
"4. Om texten är obegriplig med konstiga tecken eller allmänt osammanhängande." \
"5. Om texten nämner en bild som kan finnas på sidan" \
"Resonera med ca 2 meningar och ge sedan ett Ja/Nej svar för varje punkt. " \
"Förstår du formatet du ska svara på? Ge ett exempel på format." \



sys_msg = HumanMessage(
    content=[
        {
            "type": "text",
            "text": instructions,
        }, 
    ]
)

ai_example_text = "Ja jag tror jag förstår, här är ett exempel:\n" \
"1: exempel motivering, Svar: Ja/Nej, \n" \
"2: exempel motivering, Svar: Ja/Nej,\n" \
"3: exempel motivering, Svar: Ja/Nej,\n" \
"4: exempel motivering, Svar: Ja/Nej,\n" \
"5: exempel motivering, Svar: Ja/Nej" \


ai_example = AIMessage(
    content=[
        {
            "type": "text",
            "text": ai_example_text,
        },  
    ]
)

human_response = HumanMessage(
    content=[
        {
            "type": "text",
            "text": "Mycket bra, svara alltid på det formatet",
        }, 
    ]
)

ai_response = AIMessage(
    content=[
        {
            "type": "text",
            "text": "Tack, jag kommer att svara på det formatet framöver.",
        },  
    ]
)


verdicts = []

for text in texts:
    #print(text)
    response = gemini_pro.invoke([sys_msg, ai_example, human_response, ai_response, HumanMessage(content=[{"type": "text", "text": text}])])
    verdicts.append(response.content)


for i,verdict in zip(range(start_page, start_page+no_pages), verdicts):
    print(f"Verdict for page {i}:")
    print(verdict)


dump = "KandDOM/backend/tointegrate/multi_modal/txts/output_dump.txt"

with open(dump, 'w', encoding='utf-8') as file:
    for verdict in verdicts:
        file.write(verdict)
        file.write("\n\n")


binary_econdings_instructions = "Du är en assistent med en simpel uppgift, du ska göra om en serie svar till en binär sträng. Varje svar motsvarar en siffra i strängen, där 'Ja' motsvarar '1' och 'Nej' motsvarar '0'. " \
"Svaren inleds med en kort motivering och följs sedan av ett Ja/Nej svar. Varje svar har också en numrering vilket motsvarar dess ordning i den binära strängen. " \
"Ett exempel:"
"1. Jag ser inget som liknar det, Svar: Nej"
"2. Det finns en bild nämnd, Svar: Ja"
"3. Paris ligger i frankrike, Svar Ja"
"4. Det finns bevis för motsatsen, Svar: Nej"
"5. Inget utmärkande stack ut, Svar: Ja"
"Blir: 01101"


binary_sys = SystemMessage(
    content=[
        {
            "type": "text",
            "text": "Du är en assistent med en simpel uppgift, du ska göra om en serie svar på formen 'Ja' eller 'Nej' till en binär sträng. Varje svar motsvarar en siffra i strängen, där 'Ja' motsvarar '1' och 'Nej' motsvarar '0'.", \
        }, 
    ]
)

human_msg1 = HumanMessage(
    content=[
        {
            "type": "text",
            "text": "1: Ja, 2: Nej, 3: Ja, 4: Nej, 5: Ja",
        }, 
    ]
)

ai_msg1 = AIMessage(
    content=[
        {
            "type": "text",
            "text": "10101",
        },  
    ]
)


human_msg2 = HumanMessage(
    content=[
        {
            "type": "text",
            "text": "1: Nej, 2: Nej, 3: Nej, 4: Nej, 5: Nej",
        }, 
    ]
)

ai_msg2 = AIMessage(
    content=[
        {
            "type": "text",
            "text": "00000",
        },  
    ]
)


binary_encodings = []

# for verdict in verdicts:
#     result = gemini_pro.invoke([binary_sys, HumanMessage(content=[{"type": "text", "text": verdict}])])
#     binary_encodings.append(result.content)

# for i, encoding, verdict in zip(range(start_page, start_page+no_pages), binary_encodings, verdicts):
#     print(f"Binary encoding for page {i}:")
#     print("verdict: "+ verdict+" encoding: "+encoding)
