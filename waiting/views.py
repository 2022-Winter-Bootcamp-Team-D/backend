from django.db import transaction
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from backend.models import Token
from store.models import Store
from store.notification import notify
from swagger.serializer import SwaggerWaitingsPatchSerializer, SwaggerWaitingListSerializer, SwaggerWaitingsPostSerializer
from users.models import User
from waiting.models import Waiting
from waiting.serializer import WaitingSerializer


# 대기 순서
def search_waiting_order(waiting_id, store_id):
    waiting_teams = Waiting.objects.filter(waiting_id__lt=waiting_id, store_id=store_id, status="WA")
    waiting_order = len(waiting_teams) + 1
    return waiting_order


# 헤더에 있는 토큰으로 유저 객체 get
def search_user(request):
    jwt_object = JWTAuthentication()
    header = jwt_object.get_header(request) # 헤더
    raw_token = jwt_object.get_raw_token(header) # 원시 토큰
    validated_token = jwt_object.get_validated_token(raw_token) # 검증된 토큰
    user = jwt_object.get_user(validated_token) # 유저 객체
    return user


# 유저 계정 판별
def is_auth(user_data):
    if user_data.role == 'auth':
        return True
    return False


class Waitings(APIView):
    @swagger_auto_schema(tags=['Waiting'], request_body=SwaggerWaitingListSerializer)
    @transaction.atomic
    def get(self, request):
        user = search_user(request)
        role_check = is_auth(user)
        if role_check:
            # 전화 번호, 비밀 번호를 이용해서 웨이팅 중인 데이터 반환
            try:
                user_id = user.user_id
                user_data = User.objects.get(user_id=user_id)
                phone_num = user_data.phone_num
                db_data = Waiting.objects.get(phone_num=phone_num,
                                              status="WA")
            except:
                return Response("조회 결과가 없습니다.", status=404)

            waiting_id = db_data.waiting_id
            store_id = db_data.store_id
            # 대기 순서 계산
            waiting_order = search_waiting_order(waiting_id, store_id)

            db_data.waiting_order = waiting_order
            serializer = WaitingSerializer(db_data)

            return Response(serializer.data, status=200)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    @swagger_auto_schema(tags=['Waiting'], request_body=SwaggerWaitingsPostSerializer)
    @transaction.atomic
    def post(self, request):
        user = search_user(request)
        role_check = is_auth(user)
        if role_check:
            phone_num = user.phone_num
            name = user.name
            store_id = Store.objects.get(store_id=request.data["store_id"])
            people = request.data["people"]
            token = request.data['token']

            # 웨이팅 등록한  전화 번호로 이미 웨이팅이 존재할 경우
            waiting_check = Waiting.objects.filter(phone_num=phone_num, status="WA").exists()
            if waiting_check:
                return Response("웨이팅이 이미 존재합니다!", status=400)

            result = Waiting.objects.create(store_id=store_id, name=name, phone_num=phone_num,
                                            people=people, status="WA")
            Token.objects.create(waiting_id=result, token=token)
            waiting_id = result.waiting_id
            waiting_order = search_waiting_order(waiting_id, store_id)

            result.waiting_order = waiting_order
            serializer = WaitingSerializer(result)

            return Response(serializer.data, status=201)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    @swagger_auto_schema(tags=['Waiting'], request_body=SwaggerWaitingsPatchSerializer)
    @transaction.atomic
    def patch(self, request):
        user = search_user(request)
        role_check = is_auth(user)
        if role_check:
            phone_num = user.phone_num
            waiting = Waiting.objects.get(phone_num=phone_num, status='WA')
            waiting_id = waiting.waiting_id
            store_id = waiting.store_id.store_id # waiting 테이블에서 store_id가 외래키 이므로 waiting.store_id=Store(객체)이다.
            try:
                waiting_order = search_waiting_order(waiting_id, store_id)
                Waiting.objects.filter(waiting_id=waiting_id, store_id=store_id).update(status='CN')
                if waiting_order == 1:
                    # 사용자가 취소한 가게의 웨이팅 리스트 반환
                    waitings = Waiting.objects.raw(
                        """SELECT waiting_id
                        FROM Waiting 
                        WHERE store_id=%s AND status=%s""" % (store_id, "'WA'"))
                    try:
                        # 취소한 웨이팅이 1순위였고 다음 웨이팅 팀이 존재할 경우 다음 팀에게 1순위 알림 보내기
                        auto_token = Token.objects.get(waiting_id=waitings[0]).token
                        notify.auto_notify(auto_token)
                    except :
                        pass
            except:
                return Response(status=400)
            return Response("성공적으로 취소 됐습니다.", status=200)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
