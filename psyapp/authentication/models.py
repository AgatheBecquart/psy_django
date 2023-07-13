from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class BaseUser(AbstractUser):
    user_id = models.IntegerField(null=True)

    def save(self, *args, **kwargs):
        self.user_id = self.id
        super().save(*args, **kwargs)

class Psychologue(BaseUser):
    specialite = models.CharField(max_length=100)
    bio = models.TextField()

    def __str__(self):
        return self.username


class Patient(BaseUser):
    date_naissance = models.DateField()
    adresse = models.CharField(max_length=200)
    psychologue_referent = models.ForeignKey(Psychologue, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.username


