from anthropic import AnthropicVertex
#message: Message from user
#response: Response from model
#Intended to be used with the current system for pins
def pinsum(message, response):
    optind = 0
    options = ["us-central1", "europe-west4"]
    loc = options[optind]
    context = "Your purpose is to create a very short summary of the contents of a message, no more then 50 characters. Respond only with the summary and answer in Swedish."
    client = AnthropicVertex(region=loc, project_id="sunlit-inn-417922")
    while True:
        try:
            message = client.messages.create(
            max_tokens=50,
            messages= [{
                "role": "user",
                "content": message+ response
            }],
            model="claude-3-haiku@20240307",
            system = context,
            )
            return message.content[0].text
        except Exception as e:
            print("Error: ", e)
            
            
# print(pinsum(input("Enter a message to summarize: "), input("Enter a response to summarize: ")))
