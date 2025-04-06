from django.shortcuts import render
from django.shortcuts import redirect 
from django.http import JsonResponse

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import APIView

from detection.models import Emotion
from rest_framework.permissions import AllowAny 

import requests
from django.conf import settings

from openai import OpenAI

from .serializer import AutoModelSerializer
from django.utils.decorators import method_decorator
from django.middleware.csrf import get_token

class emo_response(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        input_message = AutoModelSerializer(data=request.data)
        if not input_message.is_valid():
            return JsonResponse({'errors': input_message.errors}, status=400)
        
        input_text = input_message.validated_data["emotion_input"]
        input_request_analysis = "回复要求：请用通俗易懂的语言分析这句话的情感状态，只要分析"
        input_request_comfort = "回复要求：请用通俗易懂的语言分析这句话,只给出安慰建议"
        
        client = OpenAI(api_key=settings.DEEPSEEK_API_KEY, base_url=settings.DEEPSEEK_API_URL)
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
            Emotion.objects.create(
                user='unknown',
                emotion_input=input_text,
                emotion_analysis=analysis_content,
                comfort=comfort_content
            )
            
            return JsonResponse({
                'emotion_input': input_text,
                'emotion_analysis': analysis_content,
                'comfort': comfort_content
            }, status=200)
        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': f'请求失败，请稍后再试。详情: {str(e)}'}, status=500)
        except Exception as e:
            return JsonResponse({'error': f'服务器内部错误: {str(e)}'}, status=500)

#跳转到首页
def emo_home(request):
    # 在模板中注入 CSRF Token
    csrf_token = get_token(request)
    return render(request, 'loading_website.html', {'csrf_token': csrf_token})
        
#跳转到输出页面
def emo_output(request):
    # 从 URL 参数中获取数据
    emotion_input = request.GET.get('emotion_input', '未提供情感分析输入')
    emotion_analysis = request.GET.get('emotion_analysis', '情感分析加载失败')
    comfort = request.GET.get('comfort', '言语慰藉加载失败')

    # 将数据传递到模板
    return render(request, 'output_website.html', {
        'emotion_input': emotion_input,
        'emotion_analysis': emotion_analysis,
        'comfort': comfort,
    })
