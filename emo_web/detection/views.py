from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import APIView

from detection.models import Emotion

import requests
from django.conf import settings

from openai import OpenAI

from .serializer import AutoModelSerializer

class emo_response(APIView):
    def post(self,request):
        input_message = AutoModelSerializer(data=request.data)
        if not input_message.is_valid():
            return render(request,settings.BASE_DIR/'template'/'output.html',input_message.errors)
        input_text = input_message.validated_data["emotion_input"]
        input_user = input_message.validated_data["user"]
        input_request_analysis = "回复要求：请用通俗易懂的语言分析这句话的情感状态，只要分析"
        input_request_comfort = "回复要求：请用通俗易懂的语言分析这句话,只给出安慰建议"        
        client = OpenAI(api_key=settings.DEEPSEEK_API_KEY, base_url=settings.DEEPSEEK_API_URL)
        message_analysis = f'{input_text}\n\n{input_request_analysis}'
        message_comfort = f'{input_text}\n\n{input_request_comfort}'
        try:
            # 情感分析请求
            analysis_response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[{
                    "role": "user",
                    "content": f"{input_text}\n\n{input_request_analysis}"
                }],
                temperature=0.7,
                stream=False
            )
            
            # 安慰建议请求
            comfort_response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[{
                    "role": "user",
                    "content": f"{input_text}\n\n{input_request_comfort}"
                }],
                temperature=0.7,
                stream=False
            )
            
            # 提取响应内容
            analysis_content = analysis_response.choices[0].message.content
            comfort_content = comfort_response.choices[0].message.content
            
            # 创建数据库记录
            emotion_record = Emotion.objects.create(
                user = input_user,
                emotion_input=input_text,
                emotion_analysis=analysis_content,
                comfort=comfort_content
            )
            return render(request, settings.BASE_DIR/'template'/'output.html', {
                'emotion_input': input_text,
                'emotion_analysis': analysis_content,
                'comfort': comfort_content,
                'user': input_user
            })
        except requests.exceptions.RequestException as e:
            return render(request, settings.BASE_DIR/'template'/'output.html', {
                'error': '请求失败，请稍后再试。'
            })

#跳转到首页
def emo_home(request):
    render(request, 'detection/loading website.html')
        
#跳转到输出页面
def emo_output(request):
    render(request, 'detection/output website.html')
        