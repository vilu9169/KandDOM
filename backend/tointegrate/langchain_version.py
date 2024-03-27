from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_google_vertexai import VertexAI

model = VertexAI(model_name="text-bison")



# Replace with your project ID and endpoint
endpoint = "https://us-central1-aiplatform.googleapis.com/v1/projects/sunlit-inn-417922/locations/us-central1/publishers/google/models/chat-bison:predict"

# Initialize conversation memory and chain
memory = ConversationBufferMemory()  # Stores last two messages
chain = ConversationChain(endpoint=endpoint, memory=memory)
model.

def chat():
    #Set the chains context
    dokument = ""
    with open("output.txt", "r", encoding='utf-8') as file:
        dokument = file.read()	
    chain.set_context(    context = "Du analyserar juridiska dokument för att underlätta arbete med dem. Du ska svara sakligt, opartiskt och enbart använda information från detta dokument i dina svar. Detta är det dokument :" + dokument)
    while True:
        user_input = input("You: ")
        
        # Add user input to memory
        memory.append(user_input)
        
        # Generate response using Langchain
        response = chain.next(prompt=user_input)
        
        # Print response and update memory
        print("Chat Bison:", response["text"])
        memory.append(response["text"])


if __name__ == "__main__":
  print("Welcome to Chat Bison!")
  chat()

