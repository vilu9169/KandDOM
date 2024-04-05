
from django.urls import path, include
from . views import *
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('chat/', chat_view, name='chat_view'),
    path('', index, name='index'),
    path('login/', index, name='login'),
    path('test/', display_text_file, name='display_text'),
    path('token/', jwt_views.TokenObtainPairView.as_view(), name ="token_obtain_pair"),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
    path('signup/', RegisterView.as_view(), name='register'),
    path('upload/', upload_document, name='upload')
]