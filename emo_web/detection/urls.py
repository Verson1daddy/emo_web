from django.urls import path
import template
from . import views

urlpatterns = [
    path("anlysis/", views.emo_response, name="analysis"),
    path('home/', template.input.html, name = 'home'),
    path('output/', template.output.html, name = 'output'),
    # 其他路由...
]
