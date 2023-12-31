from django.db import models
from django.utils.timezone import now
from authentication.models import Patient,Psychologue
from django_elasticsearch_dsl.registries import registry

class Text(models.Model):
    date = models.DateTimeField(default=now)
    text = models.TextField(max_length=1000)
    emotion = models.CharField(max_length=50)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    psychologue_referent = models.ForeignKey(Psychologue, on_delete=models.SET_NULL, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        TextDocument().update(self)
        
from .document import TextDocument






    


