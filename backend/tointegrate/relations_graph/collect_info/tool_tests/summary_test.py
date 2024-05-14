from time import time
from get_predictions import get_claude_prediction_string



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

people_instructions = """
Ditt jobb är att sammanställa information om personer från en text. Börja med att sammanställa vad texten handlar om i grova drag och vilka personer som nämns i texten.
Skriv sedan en rubrik för varje person som nämns i texten och skriv sedan en punktlista med information om personerna. Punkterna ska vara utförliga, försök att inkludera så
mycket information som möjligt från texten. Ange sidorna i texten där du hittade informationen för varje punkt.

Var utförlig och gör en rubrik för varje person som nämns i texten.
"""

people_instructions2 = """
Ditt jobb är att sammanställa information om personer från en text. Börja med att sammanställa vilka sidnummer texten består av och vilka personer som nämns i texten.
Skriv sedan en rubrik för varje person som nämns i texten och skriv sedan lista med vad varje sida nämner om personen. Om det inte finns någon information om personen på
sidan behöver du inte skriva något om den sidan.

exempel på format för varje person:

Person1:
- sida 32: Person1 är ett vittne till brottet
- sida 33: Person1 pratar om hur hen träffade Person2
- sida 34:  Person2 beskriver Person1
- sida 36:  Person1 delges information om brottet

Person2:...

Var utförlig och gör en rubrik för varje person som nämns i texten. Glöm inte att inleda varje punkt med vilken sida informationen kommer ifrån.
"""

relations_instructions = """
Ditt jobb är att sammanställa information om relationer och kopplingar mellan personer i text, börja med ett kort sammanfatta vad texten handlar om.
En relation består av två personer samt information om hur de är kopplade till varandra. Skriv de två personer som är inblandade i relationen som en rubrik
och beskriv sedan kopplingen mellan dem. Ge ingen information om personerna enskilt, endast kopplingen mellan dem.
Det är viktigt att du alltid svarar på svenska. Skriv all information med fullständiga meningar och ange alltid på vilken eller vilka sidor i texten du hittade informationen.
"""
text : str

file_path = "KandDOM/fuppar_txt/schizzomord.txt"

with open(file_path, "r") as file:
    text = file.read()

pages = text.split(chr(28))


to_process = ""

for x in range(0,5):
    to_process += pages[x]





start = time()
#summary = get_claude_prediction_string(to_process, people_instructions2, model="sonnet", use_vertex=False)
summary = get_claude_prediction_string(to_process, people_instructions2, model="haiku", use_vertex=True)
#summary = get_claude_prediction_string(to_process, relations_instructions, use_vertex=True)
print(summary)
print("done in", time() - start, "seconds")
