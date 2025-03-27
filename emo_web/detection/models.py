from django.db import models

# Create your models here.
class Emotion(models.Model):
    user = models.CharField(max_length=100,default='unknown')
    emotion_input = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    comfort = models.TextField()

    def __str__(self):
        return self.user