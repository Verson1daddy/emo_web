from django.urls import path
from .views import emo_response

urlpatterns = [
    path('detection/', emo_response.as_view(), name='emo_response'),
]