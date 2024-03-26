

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

@api_view(['POST'])
def chat_view(request):
    if request.method == 'POST':
        message = request.data.get('message')  # Access request data using DRF's request.data
        if message:
            response_data = {'message': f'Backend says: {message}'}
        else: response_data = {'message': 'Backend says: Hello from Django using DRF!'}
        return Response(response_data)
    return Response({'error': 'Only POST requests are allowed.'}, status=400)
   