import boto3
import json
import threading
from time import time
client = boto3.client(service_name="bedrock-runtime", region_name="us-east-1")

def ask_question(client, model_id, prompt):
    response = client.invoke_model(
        modelId=model_id,
        body=json.dumps(
            {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 10,
                "system" : "You are a frenchman that can not speak english",
                "messages": [
                    # {
                    #     "role" : "system",
                    #     "content": [{"type": "text", "text": "You are a frenchman that can not speak english"}],
                    # },
                    {
                        "role": "user",
                        "content": [{"type": "text", "text": prompt}],
                    }
                ],
            }
        ),
    )

    result = json.loads(response.get("body").read())
    output_list = result.get("content", [])
    for output in output_list:
        print(output["text"])
model_id = "anthropic.claude-3-haiku-20240307-v1:0"


prompt = "what is the capital of france?"

threads = [threading.Thread(target=ask_question, args=[client, model_id, prompt]) for _ in range(1)]

start = time()
for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

print("time elapsed:", time() - start)



