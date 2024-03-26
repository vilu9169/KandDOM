from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
# Create your views here.
@api_view(['POST'])
def chat_view(request):
    if request.method == 'POST':
        message = request.data.get('message')  # Access request data using DRF's request.data
        if message:
            response_data = {'message': f'Backend says: {message}'}
        else: response_data = {'message': 'Backend says: Hello from Django using DRF!'}
        return Response(response_data)
    return Response({'error': 'Only POST requests are allowed.'}, status=400)