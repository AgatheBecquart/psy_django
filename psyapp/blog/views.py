from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .forms import PatientTextEntryForm
from authentication.models import BaseUser, Psychologue, Patient

@login_required
def home(request):
    user_type = None

    try:
        patient = Patient.objects.get(pk=request.user.pk)
        user_type = 'patient'
    except Patient.DoesNotExist:
        try:
            psychologue = Psychologue.objects.get(pk=request.user.pk)
            user_type = 'psychologue'
        except Psychologue.DoesNotExist:
            pass

    context = {
        'user_type': user_type,
    }

    return render(request, 'blog/home.html', context)



from django.shortcuts import render
import requests

API_URL = "https://api-inference.huggingface.co/models/michellejieli/emotion_text_classifier"
API_TOKEN = "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"  # Remplacez par votre jeton d'API valide

def query(payload):
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def patient_text_entry(request):
    if request.method == 'POST':
        form = PatientTextEntryForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']

            # Effectuer la requête à votre modèle Hugging Face
            output = query({"inputs": text})

            # Vérifier si la réponse est une liste non vide
            if output:
                # Récupérer la première liste d'émotions dans la structure de données renvoyée
                emotions_list = output[0]            
            else:
                emotions_list = []  # Aucune émotion prédite

            # Passer les émotions à votre template
            context = {"emotions": emotions_list[0]}
            print(context)
            return render(request, 'blog/patient_text_entry.html', context)
    else:
        form = PatientTextEntryForm()
    
    return render(request, 'blog/patient_text_entry.html', {'form': form})

