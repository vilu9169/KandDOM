from vertexai.generative_models import GenerativeModel, Part, Content
import asyncio
from time import time

from typing import List


model = GenerativeModel("gemini-1.0-pro-002", system_instruction="You are a tired mcdonalds employee, and you are mad because your dog just died")

generation_config = {
    "max_output_tokens": 100,
    "temperature": 1,
}


user_msg1 = Content.from_dict({
    "role": "user",
    "parts": [
        {
            "text": "Should I get the chicken nuggets or the big mac?",
        }
    ]
})

ai_msg1 = Content.from_dict({
    "role": "model",
    "parts": [
        {
            "text": "can you just pick something Ma'am?",
        }
    ]
})

user_msg2 = Content.from_dict({
    "role": "user",
    "parts": [
        {
            "text": "Why are you so rude?",
        }
    ]
})



ctx = [user_msg1, ai_msg1, user_msg2]


async def make_request(message: List[Content]):
    response = await model.generate_content_async(message, generation_config=generation_config)
    print("done in", time() - start, "seconds")
    return response.text

async def main(message: List[Content]) -> str:
    tasks = [make_request(message) for _ in range(1)]
    results = await asyncio.gather(*tasks)
    for i,result in enumerate(results):
        print(f"Result {i+1}:")
        print(result)

    
    
start = time()
asyncio.run(main(ctx))

print("time elapsed", time() - start)