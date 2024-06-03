from people import summarize_people, use_tools_on_summary, summarize_people
from util import extract_args, print_tool_call
from modify_people import Personhandler
import threading

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





def treat_tool_call(tool_call, handler: Personhandler):
    print_tool_call(tool_call)
    function = tool_call.function
    if function.name == "spara_information_om_personer":
        args = extract_args(tool_call)
        people_info = args["list_med_personer"]
        threads = []
        for person in people_info:
            name = person["förnamn"]+" "+person["efternamn"]
            information = person["information"]
            threads.append(threading.Thread(target=handler.ny_info_person, args=(name, information)))
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        print("all people treated")
    elif function.name == "spara_information_om_relationer":
        args = extract_args(tool_call)
        relation_info = args["relationer"]
        threads = []
        for relation in relation_info:
            person1 = relation["person1"]
            person2 = relation["person2"]
            name1 = person1["förnamn"]+" "+person1["efternamn"]
            name2 = person2["förnamn"]+" "+person2["efternamn"]
            relation_info = people_info["relation"]
            threads.append(threading.Thread(target=handler.ny_information_om_relation, args=(name1, name2, relation_info)))
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        print("all relations treated")
    elif function.name == "ny_information_om_gruppering":
        args = extract_args(tool_call)
        name = args.get("beskrivande_namn")
        members = args.get("gruppmedlemmar")
        info = args.get("information")
        if members is None:
            members = []
        if info is None:
            info = ""    
        handler.ny_information_om_gruppering(name, members, info)
    else:
        print(f'{function.name} not implemented yet')

def process_text(text : str, handler : Personhandler, parallel=False):
    summary = summarize_people(text)

    tool_calls = use_tools_on_summary(summary)

    for tool_call in tool_calls:
        print_tool_call(tool_call)
    threads = []
    for tool_call in tool_calls:
       threads.append(threading.Thread(target=treat_tool_call, args=(tool_call, handler)))
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    return handler.people_store, handler.relations_struct, handler.groups_store