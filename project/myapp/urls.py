
from django.urls import path
from . views import *

urlpatterns = [
    path('', display_text_file, name='display_text'),
    path('chat/', chat_view, name='chat_view'),
]