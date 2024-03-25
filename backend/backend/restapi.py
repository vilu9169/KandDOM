
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

import requests

def start_chat(project_id: str, location: str) -> str:
    # Set the endpoint URL
    #endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:streamGenerateContent "
    #Doesnt work bc no support for simple key but right otherwise
    endpoint = f"https://us-central1-aiplatform.googleapis.com/v1/projects/sunlit-inn-417922/locations/us-central1/publishers/google/models/gemini-1.0-pro:generateContent"
    #endpoint = f"https://us-central1-aiplatform.googleapis.com/v1/projects/sunlit-inn-417922/locations/us-central1/publishers/google/models/chat-bison:predict"
    

    # Set the request payload
    payload = {
    "instances": [{
        "context":  "My name is Ned. You are my personal assistant. My favorite movies are Lord of the Rings and Hobbit.",
        "examples": [ {
            "input": {"content": "Who do you work for?"},
            "output": {"content": "I work for Ned."}
        },
        {
            "input": {"content": "What do I like?"},
            "output": {"content": "Ned likes watching movies."}
        }],
        "messages": [
        {
            "author": "user",
            "content": "Are my favorite movies based on a book series?",
        }],
    }],
    "parameters": {
        "temperature": 0.3,
        "maxOutputTokens": 200,
        "topP": 0.8,
        "topK": 40
    }
    }
    payload ={
    "contents": {
        "role": "user",
        "parts": [
        {
            #Preprompt the model with example questions and answers
            
            "text": "What is the capital of France?"
        }
        ]
    }
    }

    # Set the request headers
    headers = {
        "Content-Type": "application/json",
        #Two options for getting the token
        #gcloud auth print-access-token
        #gcloud auth application-default print-access-token
        
        
        #"Authorization": "Bearer ya29.a0Ad52N3_GY5n37jM0UdgsghJ8aku0aGoBpFyEde9193mIHIg89EqW0ZCACAditspsAPLdZmQDaAlyhlF58TXktmNwPWHp0ZJt1YjHlgV0kAV-_2h3POPmPPUU4F0s5oGP77xbh60QYUoq8SB9IEyzlAJ_XMNSjFOdCbVrxQX1bW4aCgYKAVQSARESFQHGX2MiXSlJdUidBCKwsGLY1p5Z2Q0178"
        "Authorization": "Bearer ya29.a0Ad52N3-7qVPZa12Wse6BSJNQ24KZfkia7Gq4MlpP5wOBLNUKgOotIhW3ef3Rodk3qhQ6c2ytUjCrdj_eTyJ0GJDCoi_mzTEj4eTQSWsbid-nioSCgyM_VQXfrcb09Ejbhb6m8YIq3gYWYb8AZmivV7su6gij-F11yE2jaCgYKAXoSARESFQHGX2MiHTZTJzBemaPuTzEIvZbjSw0171"
    }
    print("Requesting to start the chat...")
    # Send the POST request
    #response = requests.post(endpoint, json=payload, headers=headers)
    response = requests.post(endpoint, json=payload, headers=headers)

    # Check the response status code
    if response.status_code == 200:
        return response.text
    else:
        print(response.text)
        print(response.status_code)
        return "Failed to start the chat"

# Call the function with your project ID and location
print(start_chat("sunlit-inn-417922", "europe-west4"))




# payload = {
#     "contents": {
#         "role": "user",
#         "parts": [
#         {
#         "fileData": {
#             "mimeType": "image/jpeg",
#             "fileUri": "gs://generativeai-downloads/images/scones.jpg"
#             }
#         },
#         {
#             "text": "Describe this picture."
#         }
#         ]
#     }
#     }
