from langchain_google_vertexai import ChatVertexAI
import threading
from time import time

model = ChatVertexAI(model_name="codechat-bison", convert_system_message_to_human=True, max_output_tokens=10, temperature=1.0)

results = []
def make_request(message: str):
    response = model.invoke(message)
    print("done in", time() - start, "seconds")
    results.append(response.content)

def main(message: str) -> str:
    threads = [threading.Thread(target=make_request, args=[message]) for _ in range(50)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    for result in results:
        print(result)

    
start = time()
main("hello, who are you?")

print("time elapsed", time() - start)