
from django.urls import path, re_path
from django.conf.urls import url
from . views import *
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt import views as jwt_views
from django.views.generic import TemplateView
from django.conf import settings


routes = getattr(settings, 'REACT_ROUTES', [])
urlpatterns = [
    path('chat/', chat_view, name='chat_view'),
    url(r'^(%s)?$' % '|'.join(routes), TemplateView.as_view(template_name='index.html')),
    path('test/', display_text_file, name='display_text'),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name ="token_obtain_pair"),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
    path('api/signup/', RegisterView.as_view(), name='register'),
]