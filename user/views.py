from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from elasticsearch import Elasticsearch
from .setting_bulk import inputData


@api_view(['GET'])
def search(request):
    inputData()
    es = Elasticsearch([{
        'host': 'localhost',
        'port': 9200
    }])

    search_word = request.GET['search']

    if not search_word:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'search word param is missing'})

    docs = es.search(
        index='dictionary',
        body={
            "query": {
                "multi_match": {
                    "query": search_word,
                    "fields": [
                        "store_name"
                    ]
                }
            }
        })

    data_list = []
    for data in docs['hits']['hits']:
        data_list.append(data.get('_source'))

    return Response(data_list)
