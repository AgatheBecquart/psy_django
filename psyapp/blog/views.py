from django.contrib.auth.decorators import login_required
import requests
from django.views import View
from .models import Text
from .document import TextDocument
from .forms import PatientTextEntryForm
from authentication.models import BaseUser, Psychologue, Patient
from django.utils.timezone import now
from django.shortcuts import render
from elasticsearch import Elasticsearch
import base64
from io import BytesIO
import matplotlib.pyplot as plt
from datetime import datetime


def check_user_type(request):
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

    return user_type

def home(request):
    user_type = check_user_type(request)
    context = {
        'user_type': user_type,
    }
    return render(request, 'blog/home.html', context)


API_URL = "https://api-inference.huggingface.co/models/michellejieli/emotion_text_classifier"
API_TOKEN = "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"  # Remplacez par votre jeton d'API valide

def query(payload):
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


class TextCreateView(View):
    def get(self, request):
        user_type = check_user_type(request)
        form = PatientTextEntryForm()
        return render(request, 'blog/text_form.html', {'form': form, 'user_type': user_type})

    def post(self, request):
        user_type = check_user_type(request)

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
            text_document.date = datetime.now()
            text_document.patient.psychologue_referent = patient.psychologue_referent_id
            text_document.save()

            # Passer les émotions à votre template
            context = {"emotions": emotions_list[0],"text":text, 'user_type': user_type}
            return render(request, 'blog/text_form.html', context)
        
        return render(request, 'blog/text_form.html', {'form': form, 'user_type': user_type})


def emotions_patient(request):
    user_type = check_user_type(request)
    context = {
        'user_type': user_type,
    }
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
            
            context['patient'] = patient
            context['emotion_distribution'] = emotion_distribution
            context['graphique'] = graphique
            
    return render(request, 'blog/emotions_patient.html', context)


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
    user_type = check_user_type(request)
    context = {
        'user_type': user_type,
    }
    if request.method == 'POST':
        username = request.POST.get('username', '')
        patient = get_patient_by_username(username)
        patient_id = patient.id
        emotion = request.POST.get('emotion', '')
        expression = request.POST.get('expression', '')

        texts = get_text(patient_id, emotion, expression)
        count = len(texts)

        if texts:
            context['texts'] = texts
            context['count'] = count

        return render(request, 'blog/recherche_textes.html', context)
    return render(request, 'blog/recherche_textes.html', context)

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

def emotions_dashboard(request):
    user_type = check_user_type(request)

    if request.method == 'POST':
        start_date_str = request.POST.get('start_date', '')  # Date de début au format texte
        end_date_str = request.POST.get('end_date', '')  # Date de fin au format texte
        
        # Convertir les dates en objets datetime
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        
        # Récupérer tous les patients du psychologue connecté 
        patients = Patient.objects.all()
        print(patients)
        
        # Récupérer les textes de tous les patients du psychologue sur Elasticsearch
        texts = get_all_patients_texts(patients, start_date, end_date)
            
        if texts:
            
            # Obtenir la répartition des émotions associées aux textes
            emotion_distribution = get_emotion_distribution(texts)
            
            graphique = create_bar_chart(emotion_distribution)
                    
            # Rendre le template avec les résultats
            return render(request, 'blog/emotions_dashboard.html', {'emotion_distribution': emotion_distribution, 'graphique': graphique, 'user_type': user_type})
        
        else:
            error_message = "Aucun patient actif trouvé sur la période spécifiée."
            return render(request, 'blog/emotions_dashboard.html', {'error_message': error_message, 'user_type': user_type})

    context = {
        'user_type': user_type,
    }
    
    return render(request, 'blog/emotions_dashboard.html', context)

def get_all_patients_texts(patients, start_date, end_date):
    # Connexion à Elasticsearch
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    
    # Créer une liste pour stocker les textes de tous les patients
    all_texts = []
    
    for patient in patients:
        # Requête Elasticsearch pour récupérer les textes du patient dans la plage de dates spécifiée
        query = {
            'query': {
                'bool': {
                    'must': [
                        {'term': {'patient.id': patient.id}},
                        {'range': {'date': {'gte': start_date, 'lte': end_date}}}
                    ]
                }
            },
            'size': 1000  # Nombre maximal de textes à récupérer
        }
        
        # Exécution de la recherche
        response = es.search(index='texts', body=query)
        if 'hits' in response:
            hits = response['hits']['hits']
            texts = [hit['_source'] for hit in hits]
            all_texts.extend(texts)
    
    return all_texts

import pandas as pd
import seaborn as sns

def create_bar_chart(emotion_distribution):
    # Créer une dataframe à partir de la répartition des émotions
    data = {'Emotions': list(emotion_distribution.keys()), 'Counts': list(emotion_distribution.values())}
    df = pd.DataFrame(data)

    # Vérifier s'il y a des émotions à afficher
    if df.empty:
        return None

    # Effacer le graphique précédent
    plt.clf()

    # Utiliser Seaborn pour générer le graphique en barre
    sns.barplot(x='Emotions', y='Counts', data=df)
    plt.xlabel('Emotions')
    plt.ylabel('Count')
    plt.title('Emotion Distribution')

    # Convertir le graphique en image
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    graphic = base64.b64encode(image_png).decode('utf-8')

    return graphic



# from faker import Faker
# import random

# class TextCreateView(View):
#     def get(self, request):
#         form = PatientTextEntryForm()
#         return render(request, 'blog/text_form.html', {'form': form})

#     def post(self, request):
#         form = PatientTextEntryForm(request.POST)
#         if form.is_valid():
#             text = form.cleaned_data['text']

#             # Effectuer la requête à votre modèle Hugging Face
#             output = query({"inputs": text})

#             # Vérifier si la réponse est une liste non vide
#             if output:
#                 # Récupérer la première liste d'émotions dans la structure de données renvoyée
#                 emotions_list = output[0]
#             else:
#                 emotions_list = []  # Aucune émotion prédite

#             # Enregistrer le texte dans la base de données PostgreSQL
#             patient_ids = [2, 3]  # IDs des patients à qui attribuer les textes
#             faker = Faker()

#             for patient_id in patient_ids:
#                 patient = Patient.objects.get(id=patient_id)
#                 new_text = Text.objects.create(text=text, patient=patient, psychologue_referent=patient.psychologue_referent)
#                 emotions = ['anger', 'disgust', 'fear', 'joy', 'neutral', 'sadness', 'surprise']
#                 # Enregistrer le texte dans la base Elasticsearch
#                 text_document = TextDocument(meta={'id': new_text.id})
#                 text_document.text = text
#                 text_document.emotion = random.choice(emotions)
#                 text_document.date = faker.date_time_this_year(before_now=True, after_now=False)
#                 text_document.patient.id = patient_id
#                 text_document.patient.psychologue_referent = 1
#                 text_document.save()

#             # Passer les émotions à votre template
#             context = {"emotions": emotions_list[0], "text": text}
#             return render(request, 'blog/text_form.html', context)

#         return render(request, 'blog/text_form.html', {'form': form})

# from django.test import RequestFactory

# # Créer une instance de RequestFactory
# factory = RequestFactory()

# # Créer une instance de la vue TextCreateView
# view = TextCreateView()

# faker = Faker()

# # Effectuer 100 instances de la fonction post
# for _ in range(100):
#     # Créer une requête POST factice avec des données aléatoires
#     request = factory.post('/text_create/', data={'text': faker.sentence()})

#     # Exécuter la méthode post de la vue
#     response = view.post(request)

#     # Vérifier la réponse ou effectuer d'autres opérations nécessaires

#     # Par exemple, vous pouvez imprimer la réponse
#     print(response)
    
