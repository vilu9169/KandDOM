

import os
from django.shortcuts import render
from rest_framework.response import Response

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

def test_message(request):
    return Response({'message': 'Hello, World!'})
   