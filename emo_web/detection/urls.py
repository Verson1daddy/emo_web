from django.urls import path
from . import views
from .views import emo_response

urlpatterns = [
    path('', views.emo_home, name='home'),  # 设置首页
    path("analysis/", views.emo_response.as_view(), name="analysis"),
    path('home/', views.emo_home, name = 'home'),
    path('output/', views.emo_output, name = 'output'),  # 确保路由正确
    path('emo_response/', emo_response.as_view(), name='emo_response'),
]
