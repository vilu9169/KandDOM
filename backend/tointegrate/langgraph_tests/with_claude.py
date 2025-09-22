from anthropic import AnthropicVertex
from langchain_google_vertexai import VertexAI
from langchain_anthropic import ChatAnthropic
import json


LOCATION="europe-west4" # or "europe-west4"





client = AnthropicVertex(region=LOCATION, project_id="robust-summit-417910")

message = client.messages.create(
  max_tokens=100,
  system="You are a grumpy assistant that refuses to cooperate.",
  messages=[
    {
      "role": "user",
      "content": "Send me a recipe for banana bread.",
    },
    {
      "role": "assistant",
      "content": "Find one yourself.",
    },
    {
        "role": "user",
        "content": "What's with the attitude? Rough day?",
    }
  ],
  model="claude-3-haiku@20240307",
)
print(message.content[0].text)
