from anthropic import AnthropicVertex
from time import time

start = time()


LOCATION="europe-west4"
PROJECT = "robust-summit-417910"

client = AnthropicVertex(region=LOCATION, project_id=PROJECT)

message = client.messages.create(
  max_tokens=1024,
  messages=[
    {
      "role": "user",
      "content": "Send me a recipe for banana bread.",
    }
  ],
 # model="claude-3-haiku@20240307",
  model="claude-3-sonnet@20240229"
)

print(message.content[0].text)

print(message.model_dump_json(indent=2))

print("done in", time() - start, "seconds")