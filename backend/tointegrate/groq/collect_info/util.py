import json

def print_tool_call(tool_call):
    out = ""
    name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)
    out += name+"("
    for arg in args:
        out += arg+": '"+args[arg]+"',"
    print(out[:-1]+")")