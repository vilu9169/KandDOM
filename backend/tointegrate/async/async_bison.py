from vertexai.language_models import ChatModel
import asyncio
from time import time

model = ChatModel.from_pretrained("chat-bison@002")

chat = model.start_chat(max_output_tokens=10, temperature=1.0)

async def make_request(message: str):
    response = await chat.send_message_async(message)
    print("done in", time() - start, "seconds")
    return response.text

async def main(message: str) -> str:
    tasks = [make_request(message) for _ in range(5)]
    results = await asyncio.gather(*tasks)
    for result in results:
        print(result)

    
start = time()
asyncio.run(main("Repeat after me : 'hello'"))

print("time elapsed", time() - start)