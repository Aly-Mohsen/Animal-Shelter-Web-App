from django.urls import path
from . import views

urlpatterns = [
    path('get-response/', views.chat, name='chat'),
    path('chat/', views.chat_page, name='chat_page'),
]
