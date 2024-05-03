from people import summarize_people_gemini, use_tools_on_summary
from util import extract_args, print_tool_call
from modify_people import Personhandler



def process_text(text : str, handler : Personhandler):
    summary = summarize_people_gemini(text)

    tool_calls = use_tools_on_summary(summary)

    for tool_call in tool_calls:
        print_tool_call(tool_call)

    for tool_call in tool_calls:
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
            relation = args["beskrivning av relation"]
            handler.ny_information_om_relation(person1, person2, relation)
        elif function.name == "ny_information_om_gruppering":
            args = extract_args(tool_call)
            name = args["namn"]
            members = args["gruppmedlemmar"]
            handler.ny_information_om_gruppering(name, members)
        else:
            print(f'{function.name} not implemented yet')
    return handler.people_store, handler.relations_struct, handler.groups_store