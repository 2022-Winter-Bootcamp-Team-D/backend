import requests
from django.core.cache import cache
from django.db import transaction
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.settings import api_settings

from backend.models import Token
from store.models import Store
from store.notification import notify
from swagger.serializer import SwaggerWaitingsPostSerializer
from waiting.models import Waiting
from waiting.serializer import WaitingSerializer
from swagger.serializer import header_authorization


# 대기 순서
def search_waiting_order(waiting_id, store_id):
    waiting_teams = Waiting.objects.filter(
        waiting_id__lt=waiting_id, store_id=store_id, status="WA")
    waiting_order = len(waiting_teams) + 1
    return waiting_order


# 헤더에 있는 토큰으로 유저 객체 get
def search_user(request):
    jwt_object = JWTAuthentication()
    header = jwt_object.get_header(request)  # 헤더
    raw_token = jwt_object.get_raw_token(header)  # 원시 토큰
    validated_token = get_validated_token(raw_token)  # 검증된 토큰
    user = jwt_object.get_user(validated_token)  # 유저 객체
    return user


def get_validated_token(raw_token):
    for AuthToken in api_settings.AUTH_TOKEN_CLASSES:
        try:
            return AuthToken(raw_token)
        except TokenError:
            raw_token = str(raw_token)
            raw_token = raw_token[1:]
            raw_token = raw_token.replace("'", "")
            refresh_token = cache.get(raw_token)
            if refresh_token is not None:
                refresh = {
                    "refresh": refresh_token
                }
                url = 'http://127.0.0.1:8000/api/v1/auth/user/refresh/'
                response = requests.request(
                    method='post', url=url, data=refresh)
                access_token = response.text
                access_token = access_token[11:]
                access_token = access_token[:-2]
                cache.set(access_token, refresh_token, 60 * 60 * 3)
                raise Exception(access_token)
            else:
                raise Exception("로그인 하세용")


class Waitings(APIView):
    @swagger_auto_schema(tags=['Waiting'], manual_parameters=[header_authorization()])
    @transaction.atomic
    def get(self, request):
        user = search_user(request)
        # 전화 번호, 비밀 번호를 이용해서 웨이팅 중인 데이터 반환
        try:
            phone_num = user.phone_num
            db_data = Waiting.objects.get(phone_num=phone_num,
                                          status="WA")
            store = Store.objects.get(store_id=db_data.store_id_id)
        except:
            return Response("조회 결과가 없습니다.", status=404)

        waiting_id = db_data.waiting_id
        store_id = store.store_id
        store_name = store.store_name
        # 대기 순서 계산
        waiting_order = search_waiting_order(waiting_id, store_id)

        db_data.waiting_order = waiting_order
        db_data.store_name = store_name
        serializer = WaitingSerializer(db_data)
        return Response(serializer.data, status=200)

    @swagger_auto_schema(tags=['Waiting'], request_body=SwaggerWaitingsPostSerializer,
                         manual_parameters=[header_authorization()])
    @transaction.atomic
    def post(self, request):
        user = search_user(request)
        phone_num = user.phone_num
        name = user.name
        store = Store.objects.get(store_id=request.data["store_id"])
        people = int(request.data["people"])
        token = request.data['token']

        # 웨이팅 등록한  전화 번호로 이미 웨이팅이 존재할 경우
        waiting_check = Waiting.objects.filter(
            phone_num=phone_num, status="WA").exists()
        if waiting_check:
            return Response("웨이팅이 이미 존재합니다!", status=400)

        result = Waiting.objects.create(store_id=store, name=name, phone_num=phone_num,
                                        people=people, status="WA")
        Token.objects.create(waiting_id=result, token=token)
        waiting_id = result.waiting_id
        waiting_order = search_waiting_order(waiting_id, store)

        result.waiting_order = waiting_order
        result.store_name = store.store_name
        serializer = WaitingSerializer(result)
        return Response(serializer.data, status=201)

    @swagger_auto_schema(tags=['Waiting'], manual_parameters=[header_authorization()])
    @transaction.atomic
    def patch(self, request):
        user = search_user(request)
        phone_num = user.phone_num
        waiting = Waiting.objects.get(phone_num=phone_num, status='WA')
        waiting_id = waiting.waiting_id
        # waiting 테이블에서 store_id가 외래키 이므로 waiting.store_id=Store(객체)이다.
        store_id = waiting.store_id.store_id
        try:
            waiting_order = search_waiting_order(waiting_id, store_id)
            Waiting.objects.filter(waiting_id=waiting_id,
                                   store_id=store_id).update(status='CN')
            if waiting_order == 1:
                # 사용자가 취소한 가게의 웨이팅 리스트 반환
                waitings = Waiting.objects.raw(
                    """SELECT waiting_id
                    FROM Waiting 
                    WHERE store_id=%s AND status=%s""" % (store_id, "'WA'"))
                try:
                    # 취소한 웨이팅이 1순위였고 다음 웨이팅 팀이 존재할 경우 다음 팀에게 1순위 알림 보내기
                    auto_token = Token.objects.get(
                        waiting_id=waitings[0]).token
                    notify.auto_notify(auto_token)
                except:
                    pass
        except:
            return Response(status=400)
        return Response("성공적으로 취소 됐습니다.", status=200)
