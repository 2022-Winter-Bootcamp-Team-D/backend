from rest_framework.decorators import api_view
from rest_framework.response import Response

from store.models import Store
from store.notification import notify
from user.models import User
from waiting.models import Waiting
from waiting.serializer import WaitingSerializer


def search_waiting_order(waiting_id, store_id):
    waiting_teams = Waiting.objects.filter(waiting_id__lt=waiting_id, store_id=store_id, status="WA")
    waiting_order = len(waiting_teams) + 1
    return waiting_order


@api_view(['GET', 'POST', 'PATCH'])
def waiting(request):
    if request.method == 'POST':
        store_id = Store.objects.get(store_id=request.data["store_id"])
        phone_num = request.data['phone_num']
        name = request.data["name"]
        people = request.data["people"]
        password = request.data["password"]
        token = request.data['token']
        status = "WA"

        waiting_check = Waiting.objects.filter(phone_num=phone_num, status="WA").exists()
        if waiting_check:
            return Response("웨이팅이 이미 존재합니다!", status=400)

        result = Waiting.objects.create(store_id=store_id, name=name, phone_num=phone_num,
                                        people=people, password=password, status=status)
        User.objects.create(waiting_id=result, token=token)
        waiting_id = result.waiting_id
        waiting_order = search_waiting_order(waiting_id, store_id)

        result.waiting_order = waiting_order
        serializer = WaitingSerializer(result)

        return Response(serializer.data, status=201)

    if request.method == 'GET':
        db_data = Waiting.objects.get(phone_num=request.data["phone_num"],
                                      password=request.data["password"],
                                      status="WA")
        if db_data is None:
            return Response("조회 결과가 없습니다.", status=404)

        waiting_id = db_data.waiting_id
        store_id = db_data.store_id
        waiting_order = search_waiting_order(waiting_id, store_id)

        db_data.waiting_order = waiting_order
        serializer = WaitingSerializer(db_data)

        return Response(serializer.data, status=200)

    if request.method == 'PATCH':
        waiting_id = request.data['waiting_id']
        store_id = request.data['store_id']

        try:
            waiting_order = search_waiting_order(waiting_id, store_id)
            cancel_token = User.objects.get(waiting_id=waiting_id).token
            Waiting.objects.filter(waiting_id=waiting_id, store_id=store_id).update(status='CN')
            waiting_exist = True
            try:
                # 사용자가 취소한 가게의 웨이팅 리스트 반환
                waitings = Waiting.objects.raw(
                    """SELECT waiting_id
                    FROM Waiting 
                    WHERE store_id=%s AND status=%s""" % (store_id, "'WA'"))
                auto_token = User.objects.get(waiting_id=waitings[0]).token
            except :
                waiting_exist = False

            # 취소한 웨이팅이 1순위였고 다음 웨이팅 팀이 존재할 경우 다음 팀에게 1순위 알림 보내기
            if waiting_order == 1 and waiting_exist:
                notify.auto_notify(auto_token)
        except:
            return Response(status=400)
        return Response("성공적으로 취소 됐습니다.", status=200)
