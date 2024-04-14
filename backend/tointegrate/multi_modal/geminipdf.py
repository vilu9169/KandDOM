import vertexai
from vertexai.preview.generative_models import GenerativeModel, Image
from vertexai.generative_models import GenerativeModel, Part, FinishReason

PROJECT_ID = "robust-summit-417910"
REGION = "europe-west4"
vertexai.init(project=PROJECT_ID, location=REGION)

DOC_FILE = "/home/bjorn/Code/kandarb/KandDOM/backend/tointegrate/multi_modal/jpgs/page0.jpg"
images = []
image = Image.load_from_file(DOC_FILE)

generative_multimodal_model = GenerativeModel("gemini-1.5-pro-preview-0409")

instructions = "Det här är en blankett, vi vill ha en representation av blanketten i textformat."\
"Den behöver inte se ut som blanketten men den ska innehålla motsvarande information." \
"Rader hänger ihop med varandra. Titlar för information är alltid ovanför själva inforamtionen, ibland inom samma ruta men ibland i en egen ruta." \
"Det är viktigt att rätt titel associeras med rätt information."

instructions = "Det här är en blankett. I blanketten indikerar liten text en titel (t. ex. 'namn', 'kön', 'Förtursmål') och större text värden (t. ex. 'Erik', 'Man' 'Nej)'" \
"Värden finns alltid under sin titel, antningen i samma ruta eller i rutan ovanför." \
"Titta ovanför och under text för att avgöra om det är en titel eller inte." \
"Jag kommer ställa en specifik fråga, där du bara får använda information ur formuläret för att svara, ett kort svar räcker men ge också en kort motivation. Fråga: 'Vill målsägande bli underrättad om tidpunkt för huvudförhandligen?'"

instructions = "Återge informationen i blanketten i löpande text. Det är viktigt att all information återges, svara bara på svenska med 2000 tecken."

response = generative_multimodal_model.generate_content([instructions, image])

print(response.candidates[0].text)