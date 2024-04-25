#Checks the performance of gecko against a set of language tests for swedish

#gcloud auth print-identity-token
from  langchain.embeddings.base import Embeddings
import subprocess
import requests
from typing import List


res = ""
# while res == "":
#     try :
#         print("Trying to get token")
#         res = subprocess.check_output("gcloud auth print-identity-token", shell=True, timeout=2)
#     except subprocess.TimeoutExpired:
#         res = ""
# #Convert auth to string and remove last \r\n if on windows
# if(res[-2] == 13):
#     res = res.decode("utf-8")[:-2]
# else:
#     res = res.decode("utf-8")[:-1]
#Create a new class of embeddings called Own Embedder
class ownEmbedder(Embeddings):
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        str = "http://localhost:8080/encode"# "https://kanddomembedder-k2a2qapzpa-ew.a.run.app/encode?api_key=MyCustomerApiKey"
        #&texts=["
        body = "["
        for text in texts:
            body += "\"" + text + "\","
        body = body[:-1]
        body += "]"
        #Create a http get request to the server, If no response within 1 second then retry
        #print("Token: ", res)
        headers = {"Authorization" : "Bearer " + res, "Content-Type" : "application/json", "charset" : "utf-8"}
        #Send a get request to the server, if it times out after 2 sec retry
        response = ""
        while(response == ""):
            try:
                print("Trying to get response")
                response = requests.post(str, headers=headers,json = "{\"texts\" : "+body+"}" ,timeout=20)
            except requests.exceptions.Timeout:
                response = ""
        #print(response.text)
        #Turn the string response to a list of lists of floats
        return response.json()
    def embed_query(self, texts: str) -> List[float]:
        str = "http://localhost:8080/encode"#"https://kanddomembedder-k2a2qapzpa-ew.a.run.app/encode?api_key=MyCustomerApiKey"
        #Create a http get request to the server
        #print("Token: ", res)
        headers = {"Authorization" : "Bearer " + res, "Content-Type" : "application/json", "charset" : "utf-8"}
        
        response = ""
        while(response == ""):
            try:
                print("Trying to get response")
                response = requests.post(str, headers=headers,json = "{\"texts\" : [\""+texts+"\"]}" ,timeout=10)
            except requests.exceptions.Timeout:
                response = ""
        print(response.text)
        return response.json()



import subprocess
import requests

# Load the jsonl formatted data
# Data formatted like {"category_id": 35, "question": "Jag har en allergi. Kan jag vaccinera mig?", "candidate_answers": ["Du kan vaccinera dig, men det kan vara så att vaccinet inte ger lika bra effekt som annars. Diskutera med din behandlande läkare om du undrar hur du ska göra.", "Det är inte fastställt ännu hur intygen kommer att göras tillgängliga, arbete pågår på EU-nivå kring detta. Mer information kommer.", "I nuläget gäller samma rekommendationer oavsett om du är vaccinerad eller inte. Du måste kontrollera vilka regler och rekommendationer som gäller i det landet som du ska resa till. Du måste också följa rekommendationerna som gäller för själva resan och från svenska myndigheter. Var beredd på att rekommendationerna kan ändras snabbt. Läs mer om covid-19 och resor.", "Ta med ett färskt PK-värde från ett prov som helst ska vara taget inom 7 dagar före din vaccination.", "Ja, det kan du. Men berätta för den som ska vaccinera dig att du använder blodförtunnande läkemedel. I hälsodeklarationen som du fyller i innan vaccinationen ställs också frågan. Du och den som ska vaccinera dig kan bland annat behöva diskutera när på dagen du ska vaccinera dig, beroende på vilket eller vilka läkemedel du använder.", "Kontakta myndigheterna i det land du befinner dig för att få mer information.", "Nej. Då det råder brist på vaccin så erbjuds det inte någon valmöjlighet.", "För att logga in i 1177 Vårdguidens e-tjänster behöver man ha en godkänd e-legitimation. Det finns ingen tjänst för att agera ombud, som legal ställföreträdare eller god man. Du kan istället kontakta vården på andra sätt, till exempel på telefon. Personalen hjälper till att boka tid.", "Vaccinet hinner inte skapa något skydd mot sjukdomen om du redan är smittad när du vaccinerar dig. Då kan du bli sjuk i covid-19. Du ska inte vaccinera dig om du har några symtom på covid-19. Då ska du lämna prov.", "Du vaccineras på den vårdcentral du är listad på. Det finns ett undantag för dig som vistas långvarigt (6 månader) långt ifrån din ordinarie vårdcentral och har svårt att ta dig dit för vaccination. Då kan du vända dig till närmsta vårdcentral där du vistas. Detta gäller även dig som har folkbokföringsadress på annan ort i Sverige eller utomlands. Du måste själv kontakta närliggande vårdcentral. Den vaccinatör som givit dos 1 ansvarar alltid för att planera för dos 2. Detta innebär att man inte kan vaccineras vid endast en kortvarig vistelse. I fas 4 kommer det att vara fritt att vaccinera sig var man vill. Då går det även bra att välja en vårdcentral utanför regionen, om du till exempel bor i din sommarstuga, arbetar eller studerar på annan ort.", "Du kan vaccinera dig om du ammar. Det är inte känt om vaccinerna förs över till barnet genom bröstmjölken. Men det finns inga anledningar att tro att barnet som ammas skulle få några biverkningar om du vaccineras.", "Nej det går det inte. Tider kan bokas av alla i den prioriterade gruppen som är aktuell för vaccinering, så snart bokningen öppnar.", "Ja, det kan du. Du behöver inte vara svensk medborgare för att få vaccin mot covid-19. Alla som bor eller stadigvarande vistas i Sverige kommer att erbjudas vaccin, i den prioritetsordning som Folkhälsomyndigheten rekommenderar. Även personer som söker asyl och personer som vistas utan tillstånd i Sverige kommer att erbjudas vaccination.", "Du kan bli uppringd av din vårdcentral om du tillhör en prioriterad grupp. Hur du blir kallad till vaccination kan variera, beroende på vilken vårdcentral du är listad på. När det är dags för allmänheten att vaccinera sig kommer vården inte att kalla till vaccination. Mer informatiom om hur vaccination går till i fas 4 kommer. Om du känner dig osäker på om den som ringer upp dig ringer från vårdcentralen, be om personens namn och be att få ringa upp. Lägg på luren. Kontrollera numret till din vårdcentral, ring upp och be att få prata med personen som ringde upp dig. Lämna aldrig ut några uppgifter per telefon, din vårdcentral kommer aldrig att be dig om kontonummer eller koder.", "Nej, du kan boka en tid för vaccination när tidsbokningen öppnar längre fram.", "Du som planerar en graviditet bör vaccinera dig först, innan du försöker bli gravid. Då har du skydd mot sjukdomen om du blir gravid. Det finns hittills inte något som tyder på att fostret eller den som är gravid påverkas negativt av vaccinationen. Du behöver därför inte oroa dig om det visar sig att du var gravid utan att du visste om det när du vaccinerar dig. Däremot behövs det mer kunskap för att kunna rekommendera vaccination generellt till gravida. ", "Du som är utlandssvensk bör, liksom alla andra, vaccinera dig så nära ditt hem som möjligt. Det för att minska risken för smittspridning i samband med resor. Du som är utlandssvensk och bor i ett EU/EES-land eller i Schweiz kan vaccinera dig i Sverige kostnadsfritt. Då måste du också ha ett europeiskt sjukförsäkringskort som är utfärdat i det land som du bor eller arbetar i. Detsamma gäller vissa studenter och pensionärer som har intyg från Försäkringskassan. Samma prioritetsordning för vaccinationen gäller som för de som bor i Sverige. Utlandssvenskar som bor utanför EU/EES och Schweiz kan som regel inte vaccinera sig mot covid-19 i Sverige. Undantag är personer som arbetar på vissa svenska uppdrag utomlands. Det är till exempel statligt utsända och deras familjer, missionärer, präster och volontärer i vissa länder.", "Det är din region som ansvarar för vaccinationerna. I texten När och hur kan jag vaccinera mig mot covid-19 kan du läsa mer om vilka som erbjuds vaccin i din region just nu. Se till att du har valt rätt region högst upp på sidan.", "Folkhälsomyndigheten bedömer att det är både tryggt och viktigt att använda Astra Zenecas vaccin för dig som är 65 år eller äldre. För yngre personer rekommenderas fortsatt paus. ", "Om du tillhör en prioriterad grupp kan du bli kallad. När det är dags för allmänheten att vaccineras kommer det att komma information om hur man gör för att själv ta kontakt och boka tid för vaccination. Läs mer om den vaccination som pågår just nu. Informationen uppdateras löpande.", "Din vaccination registreras för att myndigheterna och forskare ska kunna följa arbetet med vaccinationerna. Genom informationen i registret kan de få veta hur effektivt vaccinet är och om det finns biverkningar som man inte kände till. Det som registreras är ditt personnummer, vilken ort du är folkbokförd på, datum för vaccination, vilket vaccin som användes, vilken dos du fick och vilken vårdgivare som ansvarade för vaccinationen. Informationen är skyddad av sekretess. Läs mer om nationella kvalitetsregister.", " Det är viktigt att du fortsätter att följa rekommendationerna från myndigheterna även efter att du är vaccinerad.", "Västra Götalandsregionen har tillgång till samma godkända vacciner som övriga regioner i Sverige. För närvarande finns det fyra godkända vacciner i Sverige. De är från Pfizer/BionTech, Moderna, Janssen och Astra Zeneca. Det går inte att välja vilket vaccin man ska få.", "Du som har en funktionsnedsättning och inte ingår i de medicinska riskgrupperna, och som inte heller bor på särskilt boende eller har hemtjänst, blir erbjuden vaccination i samband med allmänhetens vaccination längre fram i vår.", "Just nu finns det inget sådant nationellt intyg, arbete pågår.", "Du kan vaccinera dig i en annan region eller på en annan plats än där du är skriven. Det kan till exempel vara om du arbetar eller studerar på annan ort eller bor någon annanstans på sommaren. För att få ett fullgott skydd behöver du ofta två vaccindoser med några veckors intervall mellan doserna. Det är bra om du i möjligaste mån kan vaccinera dig på samma plats vid båda vaccinationstillfällena. Det för att underlätta hälso- och sjukvårdens hantering och säkerställa att rätt vaccin finns på plats när du ska få den andra dosen.", "Personer som är 70 år eller äldre får åka sjukresetaxi till hälso- och sjukvården för vaccination mot covid-19 trots att besök för vaccination normalt inte omfattas av sjukresor. Beslutet gäller i Västra Götalandsregionen till den 30 juni 2021.", "Nästan alla som har en allergi kan vaccinera sig. Du som tidigare har fått en allvarlig allergisk reaktion som krävde vård på sjukhus kan rådgöra med en läkare innan vaccinationen. Detsamma gäller om du tidigare har fått en så kraftig reaktion efter en vaccination att du har behövt söka vård.Senare i texten kan du läsa mer om den allvarliga allergiska reaktion som kallas anafylaktisk chock.", "Nej, de vaccinen skyddar inte mot covid-19.", "Det är väldigt ovanligt med en anafylaktisk chock efter vaccinationen. Reaktionen inträffar i så fall oftast några minuter efter att du har fått vaccinet. Du ska därför stanna kvar i lokalen i 15 minuter efter att du fick vaccinationen. Personalen som vaccinerar dig vet vad de ska göra om du får en reaktion.", "Nej, du kan inte få covid-19 av vaccinet.", "Ja, alla vaccinen verkar skydda bra mot att bli svårt sjuk. Däremot är det oklart hur bra de skyddar mot att bli smittad och lindrigt sjuk. Studier pågår där det undersöks. Folkhälsomyndigheten och regionerna följer noga hur dessa varianter sprids och hur skyddet från vaccinen påverkas. ", "Du behöver inte pausa eller skjuta upp din medicinering. Men tala om vilket läkemedel du använder för den som vaccinerar.", "På Läkemedelsverket webbplats kan du läsa mer om vaccin mot covid-19. De har flera frågor och svar om innehållet i vaccinerna. "], "label": 27, "meta": {"category": "Frågor och svar om vaccination mot covid-19 (Västra Götaland)", "source": "Vårdguiden", "link": "https://www.1177.se/Vastra-Gotaland/sjukdomar--besvar/lungor-och-luftvagar/inflammation-och-infektion-ilungor-och-luftror/om-covid-19--coronavirus/om-vaccin-mot-covid-19/fragor-och-svar-om-vaccination-mot-covid-19/"}}
import json
data = []
import numpy as np

# Path to the jsonl file
file_path = "swefaq_test.jsonl"
with open(file_path, "r", encoding="utf-8") as file:
    for line in file:
        data.append(json.loads(line))
#The label is the index of the correct answer in the candidate answers
#The model should output the index of the correct answer
embedder = ownEmbedder()
total = 0
num = 0
for item in data:
    print("question: ", item["question"])
    #print("Candidate answers: ", item["candidate_answers"])
    #print("Correct answer index: ", item["label"])
    # print("Comment: ", item["meta"]["comment"])
    # print("\n")
    #Embed the input using the gecko model
    input_embedding = embedder.embed_query(item["question"])
    #Embed the candidate answers
    candansw = ""
    #Parse the comma separated candidate answers to an array of strings
    candembs = embedder.embed_documents(item["candidate_answers"])
    # for cand in item["candidate_answers"]:
    #     candembs.append(embedder.embed_query(cand))
    #Find the most similar candidate answer
    best = -1
    best_sim = -1
    for i, cand in enumerate(candembs):
        #Calculate the cosine similarity
        sim = np.array(input_embedding)@np.array(cand)
        if sim > best_sim:
            best_sim = sim
            best = i
    #print("Best answer: ", item["candidate_answers"][int(item["label"])])
    #print("Found answer: ", item["candidate_answers"][best])
    if( best == int(item["label"])):
        print("Correct")
    else:
        print("Incorrect")
    #Calculate the accuracy so far
    total += 1
    if best == int(item["label"]):
        num += 1
    print("Accuracy: ", num/total)
    
    