from django.db import models
from django.utils.timezone import now

class Text(models.Model):
    date = models.DateTimeField(default=now)
    text = models.TextField(max_length=1000)
    emotion = models.CharField(max_length=50)

    


