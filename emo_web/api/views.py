from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import APIView

from detection.models import Emotion

from .serializers import EmotionSerializer


import requests
from django.conf import settings

from openai import OpenAI


class emo_response(APIView):
    def get(self,request):
        response_dict = {}
        input_message = request.data.get('emotion_input')
        input_request_analysis = "回复要求：请用通俗易懂的语言分析这句话的情感状态，只要分析"
        input_request_comfort = "回复要求：请用通俗易懂的语言分析这句话,只给出安慰建议"        
        client = OpenAI(api_key="settings.DEEPSEEK_API_KEY", base_url="settings.DEEPSEEK_API_URL")
        message_analysis = f'{input_message}\n\n{input_request_analysis}'
        message_comfort = f'{input_message}\n\n{input_request_comfort}'
        response_analysis = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {
                    "rols":"temporary_user",
                    "content": message_analysis
                }
            ],
            stream=False,
            temperature=1.3,
        )
        response_comfort = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {
                    "rols":"temporary_user",
                    "content": message_comfort
                }
            ],
            stream=False,
            temperature=1.3,
        )
        response_dict['emotion_analysis'] = response_analysis.choices[0].message.content
        response_dict['comfort'] = response_comfort.choices[0].message.content
        return Response(response_dict.data)