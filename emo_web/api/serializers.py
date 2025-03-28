from rest_framework import serializers
from detection.models import Emotion

class EmotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emotion
        fields = '__all__'
        
        