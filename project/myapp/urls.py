
from django.urls import path
from . views import *
from .views import CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('chat/', chat_view, name='chat_view'),
    path('', index, name='index'),
    path('login/', index, name='login'),
    path('test/', display_text_file, name='display_text'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
]