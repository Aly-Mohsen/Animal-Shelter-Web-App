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
    if not user_message:
        return Response({'error': 'No message provided'}, status=400)

    # try:
    #     response = client.chat.completions.create(
    #         model="gpt-3.5-turbo",
    #         messages=[{"role": "user", "content": user_message}],
    #         max_tokens=200
    #     )
    #     ai_reply = response.choices[0].message.content.strip()
    #     return Response({'reply': ai_reply})
    # except Exception as e:
    #     return Response({'error': str(e)}, status=500)

    # Mock response for testing without actual API call
    
    ai_reply = f"Mock reply to: '{user_message}'"

    return Response({'reply': ai_reply})