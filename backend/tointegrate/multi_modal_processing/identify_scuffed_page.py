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


instructions : str = "Det här är textavläsning av en sida från ur ett förundersökningsprotokoll, din uppgift är att besvara följande fyra frågor om texten texten: " \
"1. Om texten innehåller många benämningar med korta beskrivningar, vilket kan indikera att det är ett formulär." \
"2. Om sidan innehåller ca 50 ord eller mindre totalt" \
"3. Om texten är obegriplig med konstiga tecken eller allmänt osammanhängande." \
"4. Om det finns en eller flera bildtexter som beskriver vad en bild visar" \
"Ge en kort motivering för varje svar, och svara med Ja eller Nej." \
"Ge alltid Ja/Nej svaret direkt efter motiveringen." \
"Skriv sist en sammanställning av svaren på form '1: Ja/Nej, 2: Ja/Nej, 3: Ja/Nej, 4: Ja/Nej'"\
"Svara alltid på svenska." \


sys_msg = SystemMessage(
    content=[
        {
            "type": "text",
            "text": instructions,
        }, 
    ]
)

ai_example_text = "Ja jag tror jag förstår, här är ett exempel på format:\n" \
"1: Nej texten inte ut som ett formulär, Svar: Nej, \n" \
"2: exempel motivering, Svar: Ja,\n" \
"3: exempel motivering, Svar: Nej,\n" \
"4: exempel motivering, Svar: Nej,\n" \
"1: Nej, 2: Ja, 3: Nej, 4: Nej"


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

start = time()
for text,i in zip(texts, range(len(texts))):
    #print(text)
    response = gemini_pro.invoke([sys_msg, HumanMessage(content=[{"type": "text", "text": text}])])
    verdicts.append(response.content)
    print("page", i, "done after", time() - start, "seconds")


for i,verdict in zip(range(start_page, start_page+no_pages), verdicts):
    print(f"Verdict for page {i}:")
    print(verdict)


dump = "KandDOM/backend/tointegrate/multi_modal_processing/txts/output_dump.txt"


binary_econdings_instructions = "Det här är en sammanställning svar på fyra frågor om en sida från ett förundersökningsprotokoll. " \
"Längst ned i meddelnadet finns en sammanställning av svaren på form '1: Ja/Nej, 2: Ja/Nej, 3: Ja/Nej, 4: Ja/Nej'." \
"Din uppgift är att omvandla svaren dem till en binär kod, där Ja motsvarar 1 och Nej motsvarar 0. " \
"Ange bara siffran och ingen övrig text i ditt svar."


binary_sys = SystemMessage(
    content=[
        {
            "type": "text",
            "text": binary_econdings_instructions,
        }
    ]
)


human_example = "1. Jag ser inget som liknar det, Svar: Ja\n"
"2. Det finns en bild nämnd, Svar: Nej\n"
"3. Paris ligger i frankrike, Svar Nej\n"
"4. Det finns bevis för motsatsen, Svar: Nej\n"
"Sammanställning:\n"
"1: Ja, 2: Nej, 3: Nej, 4: Nej"

human_msg1 = HumanMessage(
    content=[
        {
            "type": "text",
            "text": human_example,
        }, 
    ]
)

ai_msg1 = AIMessage(
    content=[
        {
            "type": "text",
            "text": "1000",
        },  
    ]
)


human_msg2 = HumanMessage(
    content=[
        {
            "type": "text",
            "text": "1: Nej, 2: Ja, 3: Ja, 4: Nej",
        }, 
    ]
)

ai_msg2 = AIMessage(
    content=[
        {
            "type": "text",
            "text": "0110",
        },  
    ]
)


binary_encodings = []
as_numbers = []

for verdict in verdicts:
    result = gemini_pro.invoke([binary_sys, human_msg1, ai_msg1, HumanMessage(content=[{"type": "text", "text": verdict}])])
    binary_encodings.append(result.content)
    as_numbers.append(int(result.content))
    print(time() - start, "seconds")

to_dump = ""
for i, encoding, verdict in zip(range(start_page, start_page+no_pages), binary_encodings, verdicts):
    print(f"Binary encoding for page {i}:")
    print("verdict: \n"+verdict)
    print("encoding: "+encoding)
    to_dump += f"\nBinary encoding for page {i}:\n\n" + "verdict: \n"+verdict + "\nencoding: "+encoding

with open(dump, 'a', encoding='utf-8') as file:
    file.write(to_dump)


print(as_numbers)