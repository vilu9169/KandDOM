

import os
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from django.shortcuts import get_object_or_404

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
    previous_messages = [msg['text'] for msg in messages_json[:-1]]
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

def start_chat2(input, previous_messages) -> str:
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
from .models import Document as UserDocument
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken, TokenError
from rest_framework import status
from .serializers import DocumentSerializer, MyTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenViewBase
from .models import ChatHistory, InputOutput


class RegisterView(APIView):
    def post(self, request):
        try:
            user = User.objects.get(email=request.data["email"])
        except User.DoesNotExist:
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
        access_token["user"] = UserSerializer(user).data
        print(UserSerializer(user).data)
        return Response({
            "access_token" : access_token,
            "refresh_token" : refresh_token,
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

from langchain_google_vertexai import VertexAIEmbeddings
from langchain_google_vertexai import VertexAI


from pinecone import Pinecone, ServerlessSpec, PodSpec  

pc = Pinecone(api_key="2e669c83-1a4f-4f19-a06a-42aaf6ea7e06")

#print(index.describe_index_stats())

embeddings = VertexAIEmbeddings(model_name="textembedding-gecko-multilingual@001")

        
@api_view(['POST'])
def upload_document(request):
    file_obj = request.FILES.get('file')
    print(request.data['userID'])
    
    """print("All documents in the database:")
    for document in File.objects.all():
        print(document)"""
    if file_obj:
        # Create a new Document instance
        document = UserDocument.objects.create(
            file = file_obj,
            filename=file_obj.name,
            content_type=file_obj.content_type,
            size=file_obj.size,
            timeline = []
            # file_id= ''  # You may need to provide an appropriate file ID here
        )
        
        print("Before document.save")
        print(document.file)
        document.save()
        document.timeline = handle_multi_pdfs([str(document.file)], str(document.__id__()))
        document.save()
        print("document.save complete")
        user = User.objects.get(id=request.data['userID'])
        print("User.objects.get(id=request.data['ObjectId']) COMPLETE")
        print(document.__id__())
        user.documents.add(document)  # Add the document ID to the user's documents list
        user.save()
        print(document.timeline)
        
        
        """print("All users in the database:")
        for user in User.objects.all():
            print(user)"""

        # You might want to return the ID of the newly created document for future reference
        return Response({'document_id': str(document.__id__())})
    else:
        return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def get_documents(request):
    print(request.data)
    user = User.objects.get(id=request.data['user'])
    documents = user.documents.all()
    resp = []
    for document in documents:
        print(document, document.__id__())
        id = str(document.__id__())
        resp.append({
            "id": id,
            "filename": document.filename,
            "content_type": document.content_type,
            "size": document.size,
            "uploaded_at": document.uploaded_at
        })

    return Response({'data' : resp})


class MyTokenObtainPairView(TokenViewBase):
    serializer_class = MyTokenObtainPairSerializer



from langchain_pinecone import PineconeVectorStore  
from anthropic import AnthropicVertex


llm = VertexAI()

import subprocess
import requests

@api_view(['POST'])
def start_chat(request):
    print("Starting chat")
    print(request.data.get('index_name'))
    index_name = request.data.get('index_name')
    index = pc.Index(index_name)
    group = request.data.get('group')
    vectorstore = PineconeVectorStore(  
        index, embeddings  
    )
    print("Vectorstore created")
    # Set the endpoint URL
    MODEL="claude-3-haiku@20240307"
    endpoint = f"https://us-central1-aiplatform.googleapis.com/v1/projects/sunlit-inn-417922/locations/europe-west4/publishers/anthropic/models/"+MODEL+":predict"
    context = "Du analyserar juridiska dokument för att underlätta arbete med dem. Du ska svara sakligt, opartiskt och enbart använda information från detta dokument i dina svar. Detta är de RAG delar av dokument du har att tillgå :" 
    index = 0
    prepend = ""
    append = ""
    new_message = request.data.get('message')
    messages_json = request.data.get('messages')
    for rag in vectorstore.as_retriever(search_type="mmr", search_kwargs = ({"k" : 40,})).invoke(new_message):
        #The first 10 documents are prepended to the context
        #The last 10 documents are appended to append
        if index < 10:
            prepend += rag.page_content
        elif index >10 and index < 20:
            append = rag.page_content + append
        else:
            prepend += rag.page_content
        index += 1
        #Extract text from document
    context += prepend + append
    #print("Context: ", context)
    print("Rag done")
    #Create a json struct for previous messages and the current message
    messages = []
    odd = True
    previous_messages = [msg['text'] for msg in messages_json]
    for message in previous_messages:
        if odd:
            messages.append({
                "role": "user",
                "content": message
            })
            odd = False
        else:
            messages.append({
                "role": "assistant",
                "content": message
            })
            odd = True
    messages.append({
        "role": "user",
        "content": new_message
    })

    print(request.data.get('userid'))

    LOCATION="europe-west4"

    client = AnthropicVertex(region=LOCATION, project_id="sunlit-inn-417922")

    message = client.messages.create(
    max_tokens=500,
    messages=messages,
    model="claude-3-haiku@20240307",
    system = context,
    )
    try:
        history = ChatHistory.objects.get(embedding_id=index_name)
    except ChatHistory.DoesNotExist:
        history = ChatHistory.objects.create(
            user_id=request.data.get('userid'),  # Assuming the user is authenticated
            embedding_id=index_name,  # Assuming embedding_id is defined elsewhere
        )

    inputoutput = InputOutput.objects.create(
        message= new_message,
        response = message.content[0].text
    )
    history.inputoutput.add(inputoutput)
    return Response({"message" : message.content[0].text})

from . models import GroupChatHistory
@api_view(['POST'])
def get_chat_history(request):
    group = request.data.get('group')
    embedding_id = request.data.get('embedding_id')
    try:
        if group:
            history = GroupChatHistory.objects.get(embedding_id=embedding_id)
        else:
            history = ChatHistory.objects.get(embedding_id=embedding_id)
    except ChatHistory.DoesNotExist:
        raise ValueError({'error': 'Chat history not found'})
    inputoutput = history.inputoutput.all()
    resp = []
    pinned = []
    for io in inputoutput:
        resp.append({
            "pinned": io.pinned,
            "id": io.id,
            "text": io.message,
            "user": True
        })
        resp.append({
            "text": io.response,
            "user": False
        })
        if io.pinned:
            pinned.append({'id':io.id})
    print(resp)
    return Response({'messages' : resp, 'pinned': pinned})


"""@api_view(['POST'])
def set_pinned(request):
    message_id = request.data.get('id')
    try:
        io = InputOutput.objects.get(id=message_id)
    except InputOutput.DoesNotExist:
        raise ValueError({'error':'no IO matching found'})
    io.pinned = not io.pinned
    io.save()
    return Response({'response':'Successfully pinned'})"""
    
@api_view(['POST'])
def set_pinned(request):
    try:
        message_id = request.data.get('id')
        io = InputOutput.objects.get(id=message_id)
        io.pinned = not io.pinned
        io.save()
        # Proceed with your logic here
        return Response({'success': True})
    except InputOutput.DoesNotExist:
        return Response({'error': 'InputOutput matching query does not exist.'}, status=400)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

from bson import ObjectId
import os
@api_view(['POST'])
def delete_document(request):
    document_id = request.data.get('fileid')
    user = request.data.get('user')
    print(document_id)
    try:
        document = UserDocument.objects.get(_id=ObjectId(document_id))
    except UserDocument.DoesNotExist:
        raise ValueError({'error': 'Document not found'})
    try:
        user = User.objects.get(id=user)
    except User.DoesNotExist:
        raise ValueError({'error': 'Error no user found'})
    try:
        doc_group = User.document_groups
        for group in doc_group:
            if document in group.documents:
                print(group)
                print(group.documents)
                group.documents.remove(document)
    except:
        pass
    user.documents.remove(document)
    user.save()

    if os.path.exists(str(document.file)):
        os.remove(str(document.file))
    else:
        print("The file does not exist")
    pc.delete_index(document_id)
    document.delete()
    try:
        chat = ChatHistory.objects.get(embedding_id=document_id)
    except ChatHistory.DoesNotExist:
        return Response({'message': 'Document deleted, no chat deleted'})
    for io in chat.inputoutput.all():
        io.delete()
    chat.delete()

    return Response({'message': 'Document deleted successfully'})

@api_view(['POST'])
def renameDocument(request):
    document_id = request.data.get('document_id')
    new_name = request.data.get('new_name')

    # Check if both document ID and new name are provided
    if not document_id or not new_name:
        return Response({'error': 'Both document ID and new name are required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Retrieve the document from the database
        document = UserDocument.objects.get(_id=ObjectId(document_id))
    except UserDocument.DoesNotExist:
        return Response({'error': 'Document not found'}, status=status.HTTP_404_NOT_FOUND)

    # Update the document's name
    document.filename = new_name

    # Save the document to persist the changes
    document.save()

    return Response({'message': 'Document renamed successfully'})

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

from pinecone import Pinecone, ServerlessSpec
import PyPDF2
# pdf_file = "gbg_mordforsok.pdf"
# output_file = "output.pdf"
import os
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain.schema.document import Document
from pinecone import Pinecone, ServerlessSpec
from langchain.text_splitter import RecursiveCharacterTextSplitter

def extract_text_from_pdf(pdf_file) -> str:
    try:
        with open(pdf_file, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            num_pages = len(reader.pages)
            text = ""
            #Separate pages so they start with { and end with }
            for page_num in range(num_pages):
                text += "{pagestart nr "+ str(page_num+1) +"}"
                page = reader.pages[page_num]
                text += page.extract_text()
                text +="{pageend nr "+ str(page_num+1) +"}"

            return text
    except FileNotFoundError:
        print(f"Error: File '{pdf_file}' not found.")
        return None
    
def text_to_rag(new_index_name, text):
    os.environ["PINECONE_API_KEY"] = "2e669c83-1a4f-4f19-a06a-42aaf6ea7e06"
    os.environ["PINECONE_ENV"] = "default"
    pc = Pinecone(api_key="2e669c83-1a4f-4f19-a06a-42aaf6ea7e06")
    pc.create_index(
        name=new_index_name,
        dimension=768,
        metric="cosine",
        spec=ServerlessSpec(
            cloud='aws', 
            region='us-west-2'
        ) 
    ) 
    # Split documents
    #text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=0)
    #splits = [Document(page_content=x) for x in text_splitter.split_text(text)]
    text_splitter = RecursiveCharacterTextSplitter(separators=["{pagestart", "{pageend"], chunk_overlap = 150)
    splits = [Document(page_content=x) for x in text_splitter.split_text(text)]
    #splits = text_splitter.split_text(text)    
    embeddings = VertexAIEmbeddings(model_name="textembedding-gecko-multilingual@001")
    # initialize pinecone
    vectorstore = PineconeVectorStore(new_index_name, embeddings.embed_query, splits)
    # Vertex AI embedding model  uses 768 dimensions`
    vectorstore = vectorstore.from_documents(splits, embeddings, index_name=new_index_name)
    

from . preprocessor import handle_multi_pdfs
@api_view(['POST'])
def getTimeLine(request):
    documentID = request.data.get('documentID')
    try:
        print("get doc")
        document = UserDocument.objects.get(_id=ObjectId(documentID))
    except UserDocument.DoesNotExist:
        print("no doc")
        raise ValueError({'error': 'Document not found'})
    if document.timeline is None:
        print("start make timeline")
        timeline = handle_multi_pdfs([str(document.file)], str(document.__id__()))
        document.timeline = timeline
        document.save()
        print("done timeline")
    else:
        timeline = document.timeline
    print(timeline)
    return Response({'timeline': timeline})

from .models import DocumentGroup

@api_view(['POST'])
def createDocumentGroup(request):
    name = request.data.get('name')
    userID = request.data.get('user')
    current_doc = request.data.get('current')
    new_doc = request.data.get('new_doc')
    current = request.data.get('current')
    document_group = DocumentGroup.objects.create(
        name=name,
    )
    doc = UserDocument.objects.get(_id=ObjectId(new_doc))
    doc2 = UserDocument.objects.get(_id=ObjectId(current_doc))
    document_group.documents.add(doc)
    document_group.documents.add(doc2)
    document_group.save()
    handle_multi_pdfs([str(doc.file), str(doc2.file)], str(document_group.__id__()))
    try:
        user = User.objects.get(id=userID)
        user.document_groups.add(document_group)
    except User.DoesNotExist:
        raise ValueError({'error': 'User not found'})
    return Response({'message': 'Document group created successfully', 'docID': str(document_group.__id__())})

@api_view(['POST'])
def updateDocumentGroup(request):
    groupID = request.data.get('docgroup')
    new_doc = request.data.get('new_doc')
    new_doc_obj = UserDocument.objects.get(_id=ObjectId(new_doc))
    document_group = DocumentGroup.objects.get(_id=ObjectId(groupID))
    document_group.documents.add(new_doc_obj)
    alldocs = document_group.documents.all()
    documents = []
    for doc in alldocs:
        documents.append(str(doc.file))
    document_group.save()
    handle_multi_pdfs(documents, str(document_group.__id__()))
    return Response({'message': 'Document group updated successfully'})

@api_view(['POST'])
def getDocumentGroups(request):
    user = request.data.get('user')
    document_groups = User.objects.get(id=user).document_groups.all()
    resp = []
    for group in document_groups:
        resp.append({
            "id": str(group.__id__()),
            "name": group.name,
            "documents": [str(doc.__id__()) for doc in group.documents.all()]
        })
    return Response({'data': resp})

@api_view(['POST'])
def deleteDocgroup(request):
    user = request.data.get('user')
    docGroup = request.data.get('docGroup')
    documet_group = DocumentGroup.objects.get(_id=ObjectId(docGroup))
    user = User.objects.get(id=user)
    user.document_groups.remove(documet_group)
    documet_group.delete()

@api_view(['POST'])
def getDocumentsInGroup(request):
    group = request.data.get('group')
    print('group: ', group)
    documents = DocumentGroup.objects.get(_id=ObjectId(group)).documents.all()
    resp = []
    for doc in documents:
        resp.append({
            "id": str(doc.__id__()),
            "filename": doc.filename,
            "content_type": doc.content_type,
            "size": doc.size,
            "uploaded_at": doc.uploaded_at
        })
    return Response({'data': resp})
