from django.urls import path
import template
from . import views

urlpatterns = [
    path("anlysis/", views.emo_response, name="analysis"),
    path('home/', views.emo_home, name = 'home'),
    path('output/', views.emo_output, name = 'output'),
    # 其他路由...
]
