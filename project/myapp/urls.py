
from django.urls import path
from . views import *

urlpatterns = [
    path('', display_text_file, name='display_text'),
    path('test/', test_message, name='test_message')
]