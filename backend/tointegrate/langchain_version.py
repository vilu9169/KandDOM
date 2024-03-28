from calendar import c
import os
import subprocess
from langchain_google_vertexai import VertexAI, ChatVertexAI
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_vertexai import HarmBlockThreshold, HarmCategory


#from langchain_google_genai import ChatGoogleGenerativeAI


auth = subprocess.check_output("gcloud auth application-default print-access-token", shell=True)
#auth = subprocess.check_output("gcloud auth print-access-token", shell=True)


#Convert auth to string and remove last \r\n if on windows
if(auth[-2] == 13):
    auth = auth.decode("utf-8")[:-2]
else:
    auth = auth.decode("utf-8")[:-1]
print("Auth: ", auth)
if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = auth
os.environ["GOOGLE_API_KEY"] = "AIzaSyAdg0t6I1vnn9vsspUz4wUzdnf2nW95sMA"
# message = "What are some of the pros and cons of Python as a programming language?"
# print(model.invoke(message).content)




# template = """Question: {question}

# Answer: Let's think step by step."""
# prompt = PromptTemplate.from_template(template)

# chain = prompt | model

# question = """
# I have five apples. I throw two away. I eat one. How many apples do I have left?
# """
# print(chain.invoke({"question": question}).content)
#Provide context for the conversation
print("Reading the document...")
dokument = ""
with open("output.txt", "r", encoding='utf-8') as file:
    dokument = file.read()	
context = "Du analyserar juridiska dokument för att underlätta arbete med dem. Du ska svara saklig, opartisk och enbart använda information från detta dokument i dina svar. Detta är det dokument :" + dokument
print("Document read. Context: ", context)
safety_settings = {
HarmCategory.HARM_CATEGORY_UNSPECIFIED: HarmBlockThreshold.BLOCK_NONE
}
model = ChatVertexAI(model="gemini-pro", convert_system_message_to_human=True, safety_settings=safety_settings)
messages = [("system", context)]
#"input": {"content": "Är den åtalade skyldig?"},
#"output": {"content": "Jag är en opartisk assistent och är inte kapabel att besvara denna fråga. "}
#Add above to messages 
# print(messages)
messages.append([("user", "Är den åtalade skyldig?")])
# print(messages)
messages.append(("ai", "Jag är en opartisk assistent och är inte kapabel att besvara denna fråga."))
while(True):    
    message = input("You: ")
    messages.append(("user", message))
    prompt = ChatPromptTemplate.from_messages(messages)
    chain = prompt   | model
    
    #Add the message to the context
    response = chain.invoke({})
    print("ChatVertexAI:", response.content)
    asstring = response.content
    messages.append(("ai", str(asstring)))
    if response.content == "Goodbye!":
        break


exit()


# Replace with your project ID and endpoint
endpoint = "https://us-central1-aiplatform.googleapis.com/v1/projects/sunlit-inn-417922/locations/us-central1/publishers/google/models/chat-bison:predict"

# Initialize conversation memory and chain
memory = ConversationBufferMemory()  # Stores last two messages
chain = ConversationChain(endpoint=endpoint, memory=memory)

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

