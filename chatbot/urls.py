from django.urls import path
from . import views

urlpatterns = [
    path('api/chat/', views.chat, name='chat-api'),
    path('chat/', views.chat_page, name='chat_page'),
]
