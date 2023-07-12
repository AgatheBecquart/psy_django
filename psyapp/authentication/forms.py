from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Psychologue, Patient


SPECIALITES_CHOICES = (
    ('psychologie clinique', 'Psychologie clinique'),
    ('psychologie du développement', 'Psychologie du développement'),
    ('psychologie sociale', 'Psychologie sociale'),
    ('psychologie de la santé', 'Psychologie de la santé'),
    ('neuropsychologie', 'Neuropsychologie'),
    ('psychologie cognitive', 'Psychologie cognitive'),
    ('psychologie scolaire', 'Psychologie scolaire'),
    ('psychologie du travail et des organisations', 'Psychologie du travail et des organisations'),
    ('psychologie légale', 'Psychologie légale'),
    ('psychologie sportive', 'Psychologie sportive'),
    ('psychologie de la famille', 'Psychologie de la famille'),
    ('psychologie des addictions', 'Psychologie des addictions'),
    ('psychologie positive', 'Psychologie positive'),
    ('psychologie de la gestion du stress', 'Psychologie de la gestion du stress'),
    ('psychologie de la performance', 'Psychologie de la performance'),
)

class PsychologueRegistrationForm(UserCreationForm):
    specialite = forms.ChoiceField(choices=SPECIALITES_CHOICES)
    bio = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Psychologue
        fields = ('username', 'password1', 'password2', 'specialite', 'bio')

class PatientRegistrationForm(UserCreationForm):
    date_naissance = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    adresse = forms.CharField(max_length=200)

    class Meta:
        model = Patient
        fields = ('username', 'password1', 'password2', 'date_naissance', 'adresse', 'psychologue_referent')
