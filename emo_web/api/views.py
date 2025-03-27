from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import APIView

from detection.models import Emotion
from .serializers import EmotionSerializer

def dk_api_ask

class emo_response(APIView):
    def get(self,request):
        response = request.data
        
        serializer = EmotionSerializer(response,many=True)
        return Response(serializer.data)