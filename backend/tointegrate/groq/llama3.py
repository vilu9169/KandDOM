import os

from groq import Groq

from dotenv import load_dotenv

from self_made_tools import tools

load_dotenv()

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "you are a helpful assistant",
        },
        {
            "role": "user",
            "content": "Could you tell me the score of the NBA game between the Golden State Warriors and the Los Angeles Lakers? Oh, and id also like to know the weather in San Francisco.",
        }
    ],
    tools = [tools["NBA"], tools["weather"]],
    model="llama3-70b-8192",
)

print(chat_completion.choices[0])