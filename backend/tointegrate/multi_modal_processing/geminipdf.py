import vertexai
from vertexai.preview.generative_models import GenerativeModel, Image
from vertexai.generative_models import GenerativeModel, Part, FinishReason
from time import time

PROJECT_ID = "robust-summit-417910"
REGION = "europe-west4"
vertexai.init(project=PROJECT_ID, location=REGION)

DOC_FILE = "/home/bjorn/Code/kandarb/KandDOM/backend/tointegrate/multi_modal_processing/jpgs/page2.jpg"
images = []
image = Image.load_from_file(DOC_FILE)

model_name = "gemini-1.0-pro-vision"
model_name = "gemini-1.5-pro-preview-0409"

generative_multimodal_model = GenerativeModel(model_name)

instructions_text = "Det här är en blankett, vi vill ha en representation av blanketten i textformat."\
"Den behöver inte se ut som blanketten men den ska innehålla motsvarande information." \
"Rader hänger ofta ihop med varandra. Titlar för information är alltid ovanför själva inforamtionen, ibland inom samma ruta men ibland i en egen ruta." \
"Det är viktigt att rätt titel associeras med rätt information."
"Om det finns en innehållsförteckning med sidnummer är det viktigt att sidnummren står med beskrivningen av innehållet."

instructions = "Det här är ett formulär. I formuläret indikerar liten text en titel (t. ex. 'namn', 'kön', 'Förtursmål') och större text värden (t. ex. 'Erik', 'Man' 'Nej)'" 
"Värden finns alltid under sin titel, antningen i samma ruta eller i rutan ovanför." 
"Titta ovanför och under text för att avgöra om det är en titel eller inte." 




form_instructions = "Det här är en bild av en sida från ett juridiskt dokument, din uppgift är att omvandla information till textformat."
"Om bilden innehåller ett formulär ska du sammanfatta informationen med strukturerade rubriker. " 

start = time()
response = generative_multimodal_model.generate_content([instructions_text, image])

print(response.candidates[0].text)

print("Time taken: ", time() - start)