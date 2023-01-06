import json

from django.http import JsonResponse
from rest_framework.decorators import api_view

from store.models import Store
from waiting.models import Waiting


@api_view(['GET', 'POST', 'PATCH'])
def waiting(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            store_id = Store.objects.get(store_id=data["store_id"])
            name = data["name"]
            phone_num = data["phone_num"]
            people = data["people"]
            password = data["password"]
            status = data["status"]
            Waiting.objects.create(store_id=store_id, name=name, phone_num=phone_num,
                                   people=people, password=password, status=status)

            return JsonResponse({""}, status=201)
        except Exception:
            return JsonResponse({""}, status=400)

