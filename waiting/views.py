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

    if request.method == 'GET':
        request_body = json.loads(request.body)
        db_data = Waiting.objects.get(phone_num=request_body["phone_num"],
                                      password=request_body["password"],
                                      status="WA")

        waiting_id = db_data.waiting_id
        store_id = db_data.store_id_id
        people = db_data.people
        create_at = db_data.create_at

        waiting_teams = Waiting.objects.filter(store_id=store_id, status="WA")
        waiting_order = 1
        for i in waiting_teams:
            other_waiting_id = i.waiting_id
            if other_waiting_id < waiting_id:
                waiting_order += 1

        waiting_list = [
            f"waiting_id : {waiting_id}\n",
            f"waiting_order : {waiting_order}\n",
            f"people : {people}\n",
            f"create_at : {create_at}\n"
        ]

        return HttpResponse(waiting_list, status=200)
