from langchain_google_vertexai import ChatVertexAI
import asyncio
from time import time

model = ChatVertexAI(model_name="codechat-bison", convert_system_message_to_human=True, max_output_tokens=10, temperature=1.0)


async def make_request(message: str):
    response = await model.ainvoke(message)
    print("done in", time() - start, "seconds")
    return response.content

async def main(message: str) -> str:
    tasks = [make_request(message) for _ in range(50)]
    results = await asyncio.gather(*tasks)
    for result in results:
        print(result)

    
start = time()
asyncio.run(main("hello, who are you?"))

print("time elapsed", time() - start)