
from django.urls import path
from . views import *

urlpatterns = [
    path('chat/', chat_view, name='chat_view'),
    path('', index, name='index'),
    path('test/', display_text_file, name='display_text'),
]