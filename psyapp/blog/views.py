from django.contrib.auth.decorators import login_required
import requests
from django.shortcuts import render
from django.views import View
from .models import Text
from .document import TextDocument
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


class TextCreateView(View):
    def get(self, request):
        form = PatientTextEntryForm()
        return render(request, 'blog/text_form.html', {'form': form})

    def post(self, request):
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
                
            # Enregistrer le texte dans la base de données PostgreSQL
            patient_id = request.user.id
            patient = Patient.objects.get(baseuser_ptr_id=patient_id)
            emotion = emotions_list[0]['label']
            # form.instance.patient = patient
            new_text = Text.objects.create(text=text,patient=patient,emotion=emotion,psychologue_referent=patient.psychologue_referent)
            
            # Enregistrer le texte dans la base Elasticsearch
            text_document = TextDocument(meta={'id': new_text.id})
            text_document.text = text
            text_document.score = emotions_list[0]['score']
            text_document.label = emotions_list[0]['label']
            text_document.patient.id = patient_id
            text_document.save()

            # Passer les émotions à votre template
            context = {"emotions": emotions_list[0],"text":text}
            return render(request, 'blog/text_form.html', context)
        
        return render(request, 'blog/text_form.html', {'form': form})




