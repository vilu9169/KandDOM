
from django.urls import path
from . views import *

urlpatterns = [
    path('', index, name='index'),
    path('test/', display_text_file, name='display_text'),
]