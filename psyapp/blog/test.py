from elasticsearch import Elasticsearch

# Se connecter à Elasticsearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

# Nom de l'index à interroger
index_name = 'textes'

# Requête Elasticsearch
query = {
    "query": {
        "match_all": {}
    }
}

# Exécution de la requête
response = es.search(index=index_name, body=query)

# Traitement des résultats
for hit in response['hits']['hits']:
    # Traiter chaque document ici
    document = hit['_source']
    print(document)

