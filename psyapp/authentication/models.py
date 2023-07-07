from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class Psychologue(AbstractUser):
    specialite = models.CharField(max_length=100)
    bio = models.TextField()

    groups = models.ManyToManyField(Group, related_name='psychologues')
    user_permissions = models.ManyToManyField(Permission, related_name='psychologues')

    def __str__(self):
        return self.username


class Patient(AbstractUser):
    date_naissance = models.DateField()
    adresse = models.CharField(max_length=200)
    psychologue = models.ForeignKey(Psychologue, on_delete=models.SET_NULL, null=True, blank=True)

    groups = models.ManyToManyField(Group, related_name='patients')
    user_permissions = models.ManyToManyField(Permission, related_name='patients')

    def __str__(self):
        return self.username


