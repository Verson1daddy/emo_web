from rest_framework import serializers
from .models import Emotion

class AutoModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emotion  # 替换为你的模型
        fields = '__all__'  # 自动包含所有字段