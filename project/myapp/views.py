

import os
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes

def index(request):
    return render(request, 'index.html')

def display_text_file(request):
    # Get the absolute path to the text file
    file_path = os.path.join(os.path.dirname(__file__), 'example.txt')
    # Read the contents of the text file
    with open(file_path, 'r') as file:
        text_content = file.read()
    # Pass the text content to the template
    return render(request, 'display_text.html', {'text_content': text_content})

# @api_view(['POST'])
# def chat_view(request):
#     if request.method == 'POST':
#         message = request.data.get('message')  # Access request data using DRF's request.data
#         if message:
#             response_data = {'message': f'Backend says: {message}'}
#         else: response_data = {'message': 'Backend says: Hello from Django using DRF!'}
#         return Response(response_data)
#     return Response({'error': 'Only POST requests are allowed.'}, status=400)
import json
@api_view(['POST'])
def chat_view(request):
    print('request', request)   
    print('Requst data',request.data)
    if request.method != 'POST':
        return Response({'error': 'Only POST requests are allowed.'}, status=400)
    endpoint = f"https://us-central1-aiplatform.googleapis.com/v1/projects/sunlit-inn-417922/locations/us-central1/publishers/google/models/chat-bison:predict"
    new_message = request.data.get('message')
    messages_json = request.data.get('messages')
    print('newmessage', new_message)
    print('Messages JSON: ', messages_json)
    #Load document from output.txt
    dokument = ""   
    with open("./output.txt", "r", encoding='utf-8') as file:
        dokument = file.read()	
    print('newmessage', new_message)
    #return
    #Create a context string
    context = "Du analyserar juridiska dokument för att underlätta arbete med dem. Du ska svara sakligt, opartiskt och enbart använda information från detta dokument i dina svar. Detta är det dokument :" + dokument
    #print("Context: ", context)
    #Create a json struct for previous messages and the current message
    odd = True
    messages = []
    previous_messages = [msg['text'] for msg in messages_json]
    print('Received messages: ', previous_messages)  # Get all elements except the last one
    
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
        "content": new_message
    })
    
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
    print('Messages to API: ',messages)
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
        return  Response({"message" : resp})
    else:
        print(response.text)
        print(response.status_code)
        return Response({'error' : "Failed to start the chat"})

   
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
# prevmessages = []
# while(True):
#     #Prompt user for input
#     print("Enter your message: ")
#     message = input()
#     res = start_chat(message, prevmessages)
#     prevmessages.append(message)
#     prevmessages.append(res)
#     print(res)


from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from .models import User
from .models import Document
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken, TokenError
from rest_framework import status
from .models import Document
from .serializers import DocumentSerializer



class RegisterView(APIView):
    def post(self, request):
        try:
            user = User.objects.get(email=request.data["email"])
        except user.DoesNotExist:
            serializer = UserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if user is not None:
            raise ValidationError({"detail":"User with this email already exists"})
        

class Loginview(APIView):
    def post(self, request):
        email = request.data["email"]
        password = request.data["password"]
        
        try:
            user = User.objects.get(email = email)
        except User.DoesNotExist:
            raise AuthenticationFailed("Account does  not exist")
        if user is None:
            raise AuthenticationFailed("User does not exist")
        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect Password")
        access_token = AccessToken.for_user(user)
        refresh_token =RefreshToken.for_user(user)
        return Response({
            "access_token" : access_token,
            "refresh_token" : refresh_token,
            'userID': user.id
        })
    
class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data['refresh_token']
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            return Response("Logout Successful", status=status.HTTP_200_OK)
        except TokenError:
            raise AuthenticationFailed("Invalid Token")
        
@api_view(['POST'])
def upload_document(request):
    file_obj = request.FILES.get('file')
    print(request.data['userID'])
    
    """print("All documents in the database:")
    for document in File.objects.all():
        print(document)"""
    
    if file_obj:
        # Create a new Document instance
        document = Document.objects.create(
            file = file_obj,
            filename=file_obj.name,
            content_type=file_obj.content_type,
            size=file_obj.size,
            # file_id= ''  # You may need to provide an appropriate file ID here
        )
        print("Before document.save")
        document.save(force_insert=True)
        print("document.save complete")
        user = User.objects.get(id=request.data['userID'])
        print("User.objects.get(id=request.data['ObjectId']) COMPLETE")
        print(document.id)
        user.documents.append(document.id)  # Add the document ID to the user's documents list
        user.save()
        
        
        """print("All users in the database:")
        for user in User.objects.all():
            print(user)"""

        # You might want to return the ID of the newly created document for future reference
        return Response({'document_id ': str(document._id)})
    else:
        return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
