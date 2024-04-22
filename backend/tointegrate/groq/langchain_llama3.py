from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

import asyncio
from dotenv import load_dotenv
from time import time
import os

#keys:
#bpf
#rekt

#bpf=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

#rekt=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

load_dotenv()

os.environ["GROQ_API_KEY"] = os.environ.get("bpf")


start = time()

chat = ChatGroq(temperature=0, model_name="llama3-70b-8192")

system = "You are a helpful assistant."
human = "{text}"
prompt = ChatPromptTemplate.from_messages([("human", "Write a haiku about {topic}")])
chain = prompt | chat


async def make_request(topic, key):
    print("starting request with key:", key , time() -start)
    response = await chain.ainvoke({"topic" : topic})
    print("done in", time() - start, "seconds")
    return response.content

async def main(topic) -> str:
    global chain
    tasks = [make_request(topic) for _ in range(30)]
    results1 = await asyncio.gather(*tasks)
    for result1 in results:
        print(result)
    print("SWITCHING KEYS")
    os.environ["GROQ_API_KEY"] = os.environ.get("rekt")
    new_chat = ChatGroq(temperature=0, model_name="llama3-70b-8192")
    chain = prompt | new_chat
    tasks = [make_request(topic) for _ in range(30)]
    results = await asyncio.gather(*tasks)
    for result in results:
        print(result)


asyncio.run(main("The Moon"))






# for chunk in chain.stream({"topic": "The Moon"}):
#     print(chunk.content, end="", flush=True)