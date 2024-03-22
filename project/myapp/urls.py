
from django.urls import path
from . views import display_text_file

urlpatterns = [
    path('', display_text_file, name='display_text'),
]