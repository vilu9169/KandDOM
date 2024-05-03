from anthropic import AnthropicVertex
from time import time

start = time()


LOCATION="us-east5" # or "europe-west4"
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
  model="claude-3-opus",
)
print(message.model_dump_json(indent=2))

print("done in", time() - start, "seconds")