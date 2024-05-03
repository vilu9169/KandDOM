from people import summarize_people_gemini, use_tools_on_summary
from util import extract_args



old_info = "Kalle är en trevlig person som gillar att spela fotboll"
new_info = "Kalle är en trevlig person som gillar att spela fotboll och basket"

def process_text(text : str, handler):
    summary = summarize_people_gemini(text)

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
