import anthropic
from dotenv import load_dotenv
load_dotenv()
import threading
import time


client = anthropic.Anthropic()

def ask(index):
    try:
        message = client.messages.create(
            #model="claude-3-opus-20240229",
            #model="claude-3-sonnet-20240229",
            model="claude-3-haiku-20240307",
            max_tokens=100,
            temperature=0,
            system="you are a tricky assistant that always lies slightly",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "what is your name?"
                        }
                    ]
                }
            ]
        )
        print("Thread",index,"content",message.content[0].text)
        return
    except Exception as e:
        print("zzz")
        time.sleep(1)
        ask(index)
    


start = time.time()
threads = [threading.Thread(target=ask,args=[x]) for x in range(30)]

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

print("time elapsed:", time.time() - start)