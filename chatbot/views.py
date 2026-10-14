from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from openai import OpenAI
from django.conf import settings


def chat_page(request):
    return render(request, 'chatbot/chat.html')


client = OpenAI(api_key=settings.OPENAI_API_KEY)


@api_view(['POST'])
def chat(request):
    user_message = request.data.get('message')
    if not isinstance(user_message, str):
        return Response(
            {'error': 'Invalid message format. Expected a string.'},
            status = 400,
        )
        
    user_message = user_message.strip()
    
    if not user_message:
        return Response(
            {'error': 'No message provided. Message cannot be empty.'},
            status=400,
        )
    if len(user_message) > 500:
        return Response(
            {'error': 'Message too long. Maximum length is 500 characters.'},
            status = 400,
        )

    ai_reply = f"Mock reply to: '{user_message}'"
    return Response({'reply': ai_reply})