#!/bin/sh
#curl -X DELETE "http://localhost:9200/notes"


curl -X PUT "localhost:9200/texts" -H 'Content-Type: application/json' -d'
{
    "settings": {
        "index": {
            "analysis": {
                "analyzer": {
                    "my_analyzer": {
                        "type": "standard"
                    }
                }
            },
            "number_of_shards": 1,
            "number_of_replicas": 0
        }
    },
    "mappings": {
        "properties": {
            "patient": {
                "properties": {
                    "id": {
                        "type": "integer"
                    },
                    "psychologue_referent": {
                        "type": "integer"
                    }
                }
            },
            "date": {
                "type": "date"
            },
            "text": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword"
                    }
                }
            },
            "emotion": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword"
                    }
                }
            }
        }
    }
}'

