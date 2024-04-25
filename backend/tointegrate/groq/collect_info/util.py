import json

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