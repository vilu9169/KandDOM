
# TODO(developer): Vertex AI SDK - uncomment below & run
# pip3 install --upgrade --user google-cloud-aiplatform
# gcloud auth application-default login

# import vertexai
# from vertexai.generative_models import GenerativeModel, Part


# def generate_text(project_id: str, location: str) -> str:
#     # Initialize Vertex AI
#     vertexai.init(project=project_id, location=location)
#     # Load the model
#     multimodal_model = GenerativeModel("gemini-1.0-pro-vision")
#     # Query the model
#     response = multimodal_model.generate_content(
#         [
#             # Add an example image
#             Part.from_uri(
#                 "gs://generativeai-downloads/images/scones.jpg", mime_type="image/jpeg"
#             ),
#             # Add an example query
#             "what is shown in this image?",
#         ]
#     )
#     print(response)
#     return response.text
# #Dont actually run this it devours tokens
# generate_text("sunlit-inn-417922", "us-central1")

import subprocess

import requests

def start_chat(input, previous_messages) -> str:
    endpoint = f"https://us-central1-aiplatform.googleapis.com/v1/projects/sunlit-inn-417922/locations/us-central1/publishers/google/models/chat-bison:predict"
    
    #Load document from output.txt
    dokument = ""
    with open("output.txt", "r", encoding='utf-8') as file:
        dokument = file.read()	
    
    #return
    #Create a context string
    context = "Du analyserar juridiska dokument för att underlätta arbete med dem. Du ska svara sakligt, opartiskt och enbart använda information från detta dokument i dina svar. Detta är det dokument :" + dokument
    #print("Context: ", context)
    #Create a json struct for previous messages and the current message
    messages = []
    odd = True
    for message in previous_messages:
        if odd:
            messages.append({
                "author": "user",
                "content": message
            })
            odd = False
        else:
            messages.append({
                "author": "model",
                "content": message
            })
            odd = True
    messages.append({
        "author": "user",
        "content": input
    })
    for message in messages:
        print(message)
    
    payload = {
    "instances": [{
        "context":  context,
         "examples": [ 
        #{
        #     "input": {"content": "När har konstapel Kalle interagerat med den åtalade?"},
        #     "output": {"content": "Konstapel kalle har interagerat med den åtalade vid två tillfällen. Första gången var den 12:e januari 2022 under ett förhör och andra gången var den 15:e januari 2022 då han tillkallades till bostaden."}
        # },
         {
             "input": {"content": "Är den åtalade skyldig?"},
             "output": {"content": "Jag är en opartisk assistent och är inte kapabel att besvara denna fråga. "}
         }],
        "messages": messages,
    }],
    "parameters": {
        "temperature": 0.3,
        "maxOutputTokens": 800,
        "topP": 0.8,
        "topK": 40
    }
    }
    auth = subprocess.check_output("gcloud auth application-default print-access-token", shell=True)
    
    #Convert auth to string and remove last \r\n if on windows
    if(auth[-2] == 13):
        auth = auth.decode("utf-8")[:-2]
    else:
        auth = auth.decode("utf-8")[:-1]
    # Set the request headers
    print("Auth: ", auth)
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer "+auth
    }
    response = requests.post(endpoint, json=payload, headers=headers)

    # Check the response status code
    if response.status_code == 200:
        #Get the response
        resp = response.text
        #print("Response: ", resp)
        #Response is a json object so convert it to a json object
        import json
        resp = json.loads(resp)
        #Get the response
        resp = resp["predictions"][0]["candidates"][0]["content"]
        return  resp
    else:
        print(response.text)
        print(response.status_code)
        return "Failed to start the chat"



# Call the function with your project ID and location
prevmessages = []
while(True):
    #Prompt user for input
    print("Enter your message: ")
    message = input()
    res = start_chat(message, prevmessages)
    prevmessages.append(message)
    prevmessages.append(res)
    print(res)
