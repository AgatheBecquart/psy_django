from django.conf import settings
from django.contrib.auth import login
from django.shortcuts import redirect, render

from . import forms


from django.shortcuts import render, redirect
from .forms import PsychologueRegistrationForm, PatientRegistrationForm

def psychologue_registration_view(request):
    if request.method == 'POST':
        form = PsychologueRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirigez vers la page d'accueil après l'inscription réussie
    else:
        form = PsychologueRegistrationForm()
    
    return render(request, 'authentication/psychologue_registration.html', {'form': form})


def patient_registration_view(request):
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirigez vers la page d'accueil après l'inscription réussie
    else:
        form = PatientRegistrationForm()
    
    return render(request, 'authentication/patient_registration.html', {'form': form})
