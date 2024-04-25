import os

from groq import Groq

from dotenv import load_dotenv


from time import time
load_dotenv()

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

start = time()
chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant.",
        },
        {
            "role": "user",
            "content": "Write me a haiku about the moon",
        }
    ],
    #tools = [tools["NBA"], tools["weather"]],
    model="llama3-70b-8192",
)

print(chat_completion.choices[0].message.content)

print("done in", time() - start, "seconds")