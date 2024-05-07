from dotenv import load_dotenv
load_dotenv()
import time

import threading


from openai import OpenAI
client = OpenAI()
def ask(index):
    print("thread",index,"asking")
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": "hi, who are you?"
                }
            ],
            temperature=1,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        print("Thread",index,"content",response.choices[0].message.content)
    except Exception as e:
        print(e)
        # time.sleep(1)
        # print("zzz")




start = time.time()
threads = [threading.Thread(target=ask,args=[x]) for x in range(100)]

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

print("time elapsed:", time.time() - start)