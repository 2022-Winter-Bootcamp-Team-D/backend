import json

from django.http import HttpResponse
from rest_framework.decorators import api_view

from store.models import Store
from waiting.models import Waiting


@api_view(['GET', 'POST', 'PATCH'])
def waiting(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        phone_num = data["phone_num"]
        try:
            waiting_check = Waiting.objects.filter(phone_num=phone_num, status="WA")
            if len(waiting_check) != 0:
                return HttpResponse({"이미 진행 중인 웨이팅이 있습니다!"}, status=400)
        except Waiting.DoesNotExist:
            pass

        store_id = Store.objects.get(store_id=data["store_id"])
        name = data["name"]
        people = data["people"]
        password = data["password"]
        status = data["status"]

        try:
            Waiting.objects.create(store_id=store_id, name=name, phone_num=phone_num,
                                   people=people, password=password, status=status)

            return HttpResponse(status=201)
        except Exception:
            return HttpResponse(status=400)

