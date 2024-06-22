from django.urls import path
from .views import translate_video

urlpatterns = [
    # path('translate/', translate_video, name='translate_video'),
    path('translate_video/', translate_video, name='translate_video'),
]
