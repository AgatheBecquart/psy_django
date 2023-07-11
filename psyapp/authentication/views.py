from django.conf import settings
from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
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


from django.shortcuts import get_object_or_404
from .models import Patient, Psychologue

@login_required
def register_patient(request):
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            psychologue_id = request.user.id
            patient.psychologue_referent = Psychologue.objects.get(baseuser_ptr_id=psychologue_id)
            patient.save()
            return redirect('home')
    else:
        form = PatientRegistrationForm()

    context = {
        'form': form,
    }

    return render(request, 'authentication/register_patient.html', context)





