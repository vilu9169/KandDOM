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

7. Lars Nicklas Persson
   - Vittne

Relationer och kopplingar mellan personerna:

Enligt uppgifterna i texten finns det inga tydligt beskrivna relationer eller kopplingar mellan de olika personerna.

Grupperingar av personer:

Texten nämner fem personer med efternamnet Larsson - Angela Larsson, Saga Larsson, Loke Larsson, Neo Larsson och Håkan Larsson. Detta tyder på att dessa personer troligen tillhör samma familj. Dock finns det inga ytterligare uppgifter som bekräftar detta.
"""






def treat_tool_call(tool_call, handler: Personhandler):
    print_tool_call(tool_call)
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
        relation = args["beskrivning_av_relation"]
        handler.ny_information_om_relation(person1, person2, relation)
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
    summary = page1_summary#summarize_people(text)

    tool_calls = use_tools_on_summary(summary)

    for tool_call in tool_calls:
        print_tool_call(tool_call)
    threads = []
    for tool_call in tool_calls:
       pass#threads.append(threading.Thread(target=treat_tool_call, args=(tool_call, handler)))
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    return handler.people_store, handler.relations_struct, handler.groups_store