from django.contrib.auth.decorators import login_required
import requests
from django.shortcuts import render
from django.views import View
from .models import Text
from .document import TextDocument
from .forms import PatientTextEntryForm
from authentication.models import BaseUser, Psychologue, Patient
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from django.utils.timezone import now

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
            text_document.emotion = emotion
            text_document.patient.id = patient_id
            text_document.save()

            # Passer les émotions à votre template
            context = {"emotions": emotions_list[0],"text":text}
            return render(request, 'blog/text_form.html', context)
        
        return render(request, 'blog/text_form.html', {'form': form})
    
    
from django.shortcuts import render
from elasticsearch import Elasticsearch
from .models import Patient

def emotions_patient(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        
        # Rechercher le patient dans la base de données PostgreSQL
        patient = get_patient_by_username(username)
        
        if patient:
            # Récupérer les textes du patient à partir de l'index Elasticsearch
            texts = get_patient_texts(patient.id)
            
            # Obtenir la répartition des émotions associées aux textes
            emotion_distribution = get_emotion_distribution(texts)
            
            graphique = pie_chart_view(emotion_distribution)
            
            # Rendre le template avec les résultats
            return render(request, 'blog/patient_profile.html', {'patient': patient, 'emotion_distribution': emotion_distribution, 'graphique':graphique},)
        
        else:
            error_message = "Aucun patient ne correspond à l'identifiant saisi."
            return render(request, 'blog/emotions_patient.html', {'error_message': error_message})
    
    return render(request, 'blog/emotions_patient.html')


def get_patient_by_username(username):
    try:
        patient = Patient.objects.get(username=username)
        return patient
    except Patient.DoesNotExist:
        return None


def get_patient_texts(patient_id):
    # Connexion à Elasticsearch
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    
    # Requête Elasticsearch pour récupérer les textes du patient
    query = {
        'query': {
            'term': {'patient.id': patient_id}
        },
        'size': 1000  # Nombre maximal de textes à récupérer
    }
    
    # Exécution de la recherche
    response = es.search(index='texts', body=query)
    if 'hits' in response:
        hits = response['hits']['hits']
        texts = [hit['_source'] for hit in hits]
        print(texts)
        return texts
    
    return []


def get_emotion_distribution(texts):
    emotion_distribution = {}
    
    for text in texts:
        emotion = text.get('emotion')
        if emotion:
            if emotion in emotion_distribution:
                emotion_distribution[emotion] += 1
            else:
                emotion_distribution[emotion] = 1
    print(emotion_distribution)
    return emotion_distribution


def pie_chart_view(emotion_distribution):
    plt.clf()
    # Generate the pie chart
    emotions = list(emotion_distribution.keys())
    counts = list(emotion_distribution.values())

    # Create the pie plot
    plt.pie(counts, labels=emotions, autopct='%1.1f%%')
    plt.axis('equal')

    # Convert the plot to an image
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    # Encode the image as base64
    graphic = base64.b64encode(image_png).decode('utf-8')
    
    return graphic


def recherche_textes(request):
    if request.method == 'POST':
        username = request.POST.get('username','')
        patient = get_patient_by_username(username)
        patient_id = patient.id
        emotion = request.POST.get('emotion','')
        expression = request.POST.get('expression','')
        
        texts = get_text(patient_id, emotion, expression)
        count = 0
        for text in texts : 
            count +=1
        
        return render(request, 'blog/resultat_recherche.html', {'texts':texts, 'count':count})
    return render(request, 'blog/recherche_textes.html')
        

def get_text(patient_id, emotion, expression):
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    
    query = {
        "query":{
            "bool":{
                "must":[
                    {"match":{"text":expression}},
                    {"match":{"patient.id":patient_id}},
                    {"match":{"emotion":emotion}},
                    
                ]
            }
        }
    }
   
    
    response = es.search(index='texts', body=query)
    if 'hits' in response:
        hits = response['hits']['hits']
        texts = [hit['_source'] for hit in hits]
        print(texts)
        return texts
    
    return []





