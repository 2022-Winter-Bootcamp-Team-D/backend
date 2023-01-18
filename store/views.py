from django.db import transaction
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from store.models import Store
from swagger.serializer import SwaggerStoreSigninSerializer, SwaggerStoreWaitingsPostSerializer, \
    SwaggerStoreWaitingsPatchSerializer, SwaggerStoreEnterNotifySerializer, SwaggerStoreBreakTimeSerializer, \
    SwaggerStoreDetailSerializer
from waiting.models import Waiting
from users.models import Token
from .serializer import StoreJoinSerializer
from .notification import notify


class Signin(APIView):
    @swagger_auto_schema(tags=['Store'], request_body=SwaggerStoreSigninSerializer)
    @transaction.atomic
    def post(self, request):
        store_name = request.data['store_name']
        phone_num = request.data['phone_num']
        latitude = request.data['latitude']
        longitude = request.data['longitude']
        password = request.data['password']

        try:
            object = Store.objects.create(store_name=store_name, phone_num=phone_num, latitude=latitude,
                                          longitude=longitude,
                                          password=password)
            response = StoreJoinSerializer(object)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(data=response.data, status=status.HTTP_201_CREATED)


class Enter_notify(APIView):
    @swagger_auto_schema(tags=['Store'], request_body=SwaggerStoreEnterNotifySerializer)
    @transaction.atomic
    def post(self, request):
        # result = notify.enter_notify(request)
        notify.enter_notify(token=request.data['token'])

        return Response('호출에 성공했습니다!', status=status.HTTP_200_OK)


class Breaktime(APIView):
    @swagger_auto_schema(tags=['Store'], request_body=SwaggerStoreBreakTimeSerializer)
    @transaction.atomic
    def patch(self, request):
        store_id = request.data['store_id']
        try:
            object = Store.objects.get(store_id=store_id)
            object.is_waiting = not object.is_waiting
            result = object.is_waiting
            object.save()
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(data={"is_waiting": result}, status=status.HTTP_200_OK)


class Detail(APIView):
    @swagger_auto_schema(tags=['Store'], request_body=SwaggerStoreDetailSerializer)
    @transaction.atomic
    def patch(self, request):
        store_id = request.data['store_id']
        information = request.data['information']

        try:
            object = Store.objects.get(store_id=store_id)
            object.information = information
            result = information
            object.save()
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(data={"information": result}, status=status.HTTP_200_OK)


# 가게의 웨이팅 목록, 상세정보, 웨이팅 받는지 여부를 반환
def search_waitings(store_id):
    store = Store.objects.get(store_id=store_id)
    data = {}
    data["data"] = []
    data["information"] = store.information
    data["is_waiting"] = store.is_waiting

    # 가게 웨이팅이 없을경우 상세정보랑 웨이팅 상태만 반환
    waitings = Waiting.objects.raw(
        """SELECT waiting_id
        FROM Waiting 
        WHERE store_id=%s AND status=%s ORDER BY waiting_id""" % (store_id, "'WA'"))

    for i in waitings:
        temp = {
            "waiting_id": i.pk,
            "name": i.name,
            "phone_num": i.phone_num,
            "people": i.people
        }
        data["data"].append(temp)
    return data


def search_waiting_order(waiting_id, store_id):
    waiting_teams = Waiting.objects.filter(waiting_id__lt=waiting_id, store_id=store_id, status="WA")
    waiting_order = len(waiting_teams) + 1
    return waiting_order


class Waitings(APIView):

    @swagger_auto_schema(tags=['Store'], request_body=SwaggerStoreWaitingsPostSerializer)
    @transaction.atomic
    def post(self, request):
        store_id = request.data['store_id']
        data = search_waitings(store_id)
        return Response(data, status=status.HTTP_200_OK, content_type="text/json-comment-filtered")

    @swagger_auto_schema(tags=['Store'], request_body=SwaggerStoreWaitingsPatchSerializer)
    @transaction.atomic
    def patch(self, request):
        store_id = request.data['store_id']
        waiting_id = request.data['waiting_id']
        waiting_order = search_waiting_order(waiting_id, store_id)
        try:
            waiting = Waiting.objects.get(waiting_id=waiting_id)
            waiting.status = 'EN'
            waiting.save()
            waitings = Waiting.objects.raw(
                """SELECT waiting_id, name, people, phone_num FROM Waiting WHERE store_id=%s AND status=%s LIMIT 1""" % (store_id, "'WA'"))
            try:
                second_customer = Token.objects.get(waiting_id=waitings[0]).token
                if waiting_order == 1:
                    notify.auto_notify(second_customer)
            except IndexError:
                pass
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response('대기 1순위 손님에게 알림을 보냈습니다!', status=status.HTTP_200_OK)


class Cancellations(APIView):
    @swagger_auto_schema(tags=['Store'], request_body=SwaggerStoreWaitingsPatchSerializer)
    @transaction.atomic
    def patch(self, request):
        waiting_id = request.data['waiting_id']
        store_id = request.data['store_id']
        waiting_order = search_waiting_order(waiting_id, store_id)

        cancel_token = Token.objects.get(waiting_id=waiting_id).token

        # status를 CN(CANCEL)로 바꿔주고 취소 알림 보내기
        Waiting.objects.filter(waiting_id=waiting_id, store_id=store_id).update(status='CN')
        notify.cancel_notify(cancel_token)

        # 가게의 웨이팅 리스트, 상세 정보, 웨이팅 받는지 여부를 받아 온다.
        data = search_waitings(store_id)
        try:
            auto_token = Token.objects.get(waiting_id=data["data"][0]['waiting_id']).token

            # 취소한 웨이팅이 1순위였고 다음 웨이팅 팀이 존재할 경우 다음 팀에게 1순위 알림 보내기
            if waiting_order == 1:
                notify.auto_notify(auto_token)
        # 가게의 웨이팅이 없는 경우
        except IndexError:
            pass

        return Response(data, status=status.HTTP_200_OK, content_type="text/json-comment-filtered")
