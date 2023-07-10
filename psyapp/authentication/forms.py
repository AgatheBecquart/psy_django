from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Psychologue, Patient

# Formulaire d'inscription pour les psychologues
class PsychologueRegistrationForm(UserCreationForm):
    specialite = forms.CharField(max_length=100)
    bio = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Psychologue
        fields = ('username', 'password1', 'password2', 'specialite', 'bio')

# Formulaire d'inscription pour les patients
class PatientRegistrationForm(UserCreationForm):
    date_naissance = forms.DateField()
    adresse = forms.CharField(max_length=200)

    class Meta:
        model = Patient
        fields = ('username', 'password1', 'password2', 'date_naissance', 'adresse', 'psychologue_referent')
