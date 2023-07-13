# Projet de suivi des émotions des patients pour les psychologues

Ce projet vise à fournir une plateforme permettant aux psychologues de suivre les émotions de leurs patients au fil du temps. L'application est développée en utilisant Django et utilise une base de données PostgreSQL pour enregistrer les informations sur les patients et les psychologues, ainsi qu'une base de données Elasticsearch pour stocker les textes et les évaluations.

## Fonctionnalités

L'application prend en charge les fonctionnalités suivantes :

### Pour les psychologues :
- Connexion à un espace réservé pour visualiser la répartition des émotions de tous les patients sur une certaine période de temps.
- Visualisation de la répartition des émotions d'un patient spécifique en recherchant par son nom et prénom.
- Recherche de tous les textes contenant des expressions spécifiques, avec la possibilité de filtrer par émotions et par nom/prénom de patient.
- Création d'un nouveau patient avec un mot de passe, un nom et un prénom.


### Pour les patients :
- Accès à un espace privé de connexion.
- Création d'un nouveau texte pour partager leurs émotions avec leur psychologue.
- Évaluation automatique des textes écrits par les patients à l'aide du modèle Hugging Face déployé.

## Déploiement

Pour déployer le projet en local, suivez les étapes ci-dessous :

```bash
# Assurez-vous d'avoir Python et pip installés sur votre système.
# Clonez ce référentiel depuis GitHub.
# Créez un environnement virtuel pour le projet et activez-le.
# Installez les dépendances nécessaires en exécutant la commande suivante :
pip install -r requirements.txt

# Configurez une base de données PostgreSQL et mettez à jour les informations de connexion dans les paramètres du projet.
# Configurez une base de données Elasticsearch et mettez à jour les informations de connexion dans les paramètres du projet.

# Effectuez les migrations de la base de données en exécutant les commandes suivantes :
python manage.py makemigrations
python manage.py migrate

# Démarrez le serveur de développement Django en exécutant la commande suivante :
python manage.py runserver
```
Il faudra préalablement avoir crée une base de données Postgre et ElasticSearch. 

## Auteurs : 

Manon Platteau : https://github.com/Manonp59
Agathe Becquart : https://github.com/AgatheBecquart
