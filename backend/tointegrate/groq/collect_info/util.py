import json
from vertexai import generative_models
from langchain_community.vectorstores import FAISS


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


def print_FAISS(faiss_store : FAISS):
    total_amount = faiss_store.index.ntotal
    if total_amount == 0:
        print("No entries in FAISS store")
        return
    entries = faiss_store.similarity_search("get all", total_amount)
    for entry in entries:
        print(entry.page_content)
        print("Metadata: ")
        print(entry.metadata)


gemini_unfiltered = {
    generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_NONE,
    generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_NONE,
    generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_NONE,
    generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_NONE,
}