import json
from vertexai import generative_models

def print_tool_call(tool_call):
    out = ""
    name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)
    out += name+"("
    for arg in args:
        out += arg+": '"+str(args[arg])+"',"
    print(out[:-1]+")")



def extract_args(tool_call):
    args = json.loads(tool_call.function.arguments)
    return args




gemini_unfiltered = {
    generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_NONE,
    generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_NONE,
    generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_NONE,
    generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_NONE,
}