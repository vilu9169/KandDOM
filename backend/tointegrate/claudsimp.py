from anthropic import AnthropicVertex

LOCATION="europe-west4" # or "europe-west4"

client = AnthropicVertex(region=LOCATION, project_id="sunlit-inn-417922")

message = client.messages.create(
  max_tokens=1024,
  messages=[
    {
      "role": "user",
      "content": "Send me a recipe for banana bread.",
    }
  ],
  model="claude-3-haiku@20240307",
)
print(message.model_dump_json(indent=2))