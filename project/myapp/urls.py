
from django.urls import path, re_path
from . views import *
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt import views as jwt_views
from django.views.generic import TemplateView

urlpatterns = [
    path('chat/', start_chat, name='chat_view'),
    re_path(r'^$', TemplateView.as_view(template_name='index.html')),
    re_path(r'^login$', TemplateView.as_view(template_name='index.html')),
    path('test/', display_text_file, name='display_text'),
    path('upload/', upload_document, name='upload'),
    path('api/token/', MyTokenObtainPairView.as_view(), name ="token_obtain_pair"),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
    path('api/signup/', RegisterView.as_view(), name='register'),
    path('api/documents/', get_documents, name='documents'),
    path('api/getchat/', get_chat_history, name='chat_history'),
]