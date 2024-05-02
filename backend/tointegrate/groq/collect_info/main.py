


from modify_people import Personhandler
from people import summarize_people_gemini, use_tools_on_summary
from collection_tools import tools
from util import extract_args

handler = Personhandler()

#handler.handle_ny_info_person("Kalle", "Kalle är en trevlig person som gillar att spela fotboll")

old_info = "Kalle är en trevlig person som gillar att spela fotboll"
new_info = "Kalle är en trevlig person som gillar att spela fotboll och basket"

text1 = """
Solen strålade varmt genom de stora fönstren i köket, och belyste de tre personerna som satt runt bordet och drack kaffe. Det var Maja, en ung kvinna med långt mörkt hår och glittrande ögon, hennes bror Erik, lite äldre med ett lugnt leende, och deras farmor Ingrid, en dam med visdom i blicken och rynkor runt munnen som vittnade om ett långt liv.

Maja tog en klunk av sitt kaffe och suckade. "Jag vet inte vad jag ska göra", sa hon. "Jag har sökt jobb i flera månader, men det verkar som att ingen vill ha mig."

Erik lade en hand på hennes arm. "Oroa dig inte, syster", sa han. "Du kommer att hitta något snart. Du är smart och duktig, det vet du."

Ingrid nickade instämmande. "Ja, Maja", sa hon. "Livet har en tendens att ordna upp sig på ett eller annat sätt. Fokusera på det du kan kontrollera, och resten kommer att lösa sig."

Maja log tacksamt mot dem båda. "Tack", sa hon. "Ni är alltid så snälla."

De satt tysta en stund och njöt av kaffet och varandras sällskap. Sedan reste sig Ingrid och började plocka undan disken. "Jag ska diska", sa hon. "Ni kan bara slappna av."

Maja och Erik protesterade lite, men Ingrid insisterade. När hon var klar satte hon sig ner igen och log mot sina barnbarn. "Jag älskar er båda så mycket", sa hon. "Ni är det viktigaste jag har."

Maja och Erik kramade om henne. "Vi älskar dig också, farmor", sa de.

De satt kvar en stund till och pratade och skrattade, och för en stund glömde Maja sina bekymmer. Hon var tacksam för sin familj och för det stöd de gav henne. Hon visste att hon inte var ensam, och att de alltid skulle finnas där för henne.

Solen började sjunka ner mot horisonten och kastade ett varmt sken över rummet. Det var dags att gå, men Maja ville stanna kvar lite längre. Hon ville njuta av denna stunder av frid och ro med sin familj, och minnas den för alltid.
"""


summary = summarize_people_gemini(text1)

tool_calls = use_tools_on_summary(summary)


for tool_call in tool_calls:
    function = tool_call.function
    if function.name == "ny_information_om_person":
        args = extract_args(tool_call)
        name = args["namn"]
        information = args["information"]
        handler.ny_info_person(name, information)
    elif function.name == "ny_information_om_relation":
        args = extract_args(tool_call)
        person1 = args["person1"]
        person2 = args["person2"]
        relation = args["beskrivning av relation"]
        handler.ny_information_om_relation(person1, person2, relation)
    else:
        print(f'{function.name} not implemented yet')


#result = handler._update_info(old_info, new_info)


#print(result)