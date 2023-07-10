from elasticsearch import Elasticsearch

# Créez une instance du client Elasticsearch
client = Elasticsearch()

# Nom de l'index Elasticsearch que vous souhaitez vérifier
index_name = 'textes'

# Vérifiez si l'index existe
if client.indices.exists(index=index_name):
    print(f"L'index '{index_name}' existe.")
else:
    print(f"L'index '{index_name}' n'existe pas.")
