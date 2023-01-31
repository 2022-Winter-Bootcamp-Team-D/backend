from django.contrib.auth import authenticate
from django.core.cache import cache
from django.db import transaction
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.db import connection
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from backend.models import Token
from store.models import Store
from swagger.serializer import SwaggerStoreSignupSerializer, SwaggerStoreWaitingsPatchSerializer, \
    SwaggerStoreEnterNotifySerializer, SwaggerStoreDetailSerializer, SwaggerStoreLoginSerializer, header_authorization, \
    SwaggerStoreSearchSerializer
from users.serializer import StoreUserSignupSerializer, SigninSerializer
from waiting.models import Waiting
from users.models import User
from waiting.views import search_user
from .notification import notify
from .serializer import StoreSerializer


# 가게 회원 가입
class Signup(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(tags=['Store'], request_body=SwaggerStoreSignupSerializer)
    @transaction.atomic
    def post(self, request):
        # store user 등록, 토큰 발급
        user_serializer = StoreUserSignupSerializer(data=request.data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            # jwt token 생성
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            # store 등록
            store_name = request.data['name']
            phone_num = request.data['phone_num']
            latitude = float(request.data['latitude'])
            longitude = float(request.data['longitude'])
            try:
                store = Store.objects.create(store_name=store_name, phone_num=phone_num, latitude=latitude,
                                             longitude=longitude, user_id=user)
                store_serializer = StoreSerializer(store)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            res = Response(
                {
                    "user": user_serializer.data,
                    "store": store_serializer.data,
                    "message": "register successs",
                    "access": access_token,
                },
                status=status.HTTP_201_CREATED,
            )
            cache.set(access_token, refresh_token, 60 * 60 * 3)
            return res
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


# 가게 로그인
class Login(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(tags=['Store'], request_body=SwaggerStoreLoginSerializer)
    @transaction.atomic
    def post(self, request):
        user = authenticate(
            email=request.data.get("email"), password=request.data.get("password")
        )
        if user is not None:
            store = Store.objects.get(user_id=user.id)
            store_serializer = StoreSerializer(store)
            user_serializer = SigninSerializer(user)
            user_data = User.objects.get(email=request.data.get("email"))
            role = user_data.role
            if role == 'store':
                token = TokenObtainPairSerializer.get_token(user)
                refresh_token = str(token)
                access_token = str(token.access_token)
                res = Response(
                    {
                        "user": user_serializer.data,
                        "store": store_serializer.data,
                        "message": "login success",
                        "access": access_token,
                    },
                    status=status.HTTP_200_OK,
                )
                cache.set(access_token, refresh_token, 60 * 60 * 3)
                return res
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


# 대기자 호출
class Enter_notify(APIView):
    @swagger_auto_schema(tags=['Store'], request_body=SwaggerStoreEnterNotifySerializer,
                         manual_parameters=[header_authorization()])
    @transaction.atomic
    def post(self, request):
        user = search_user(request)
        token = Token.objects.get(waiting_id=request.data['waiting_id']).token
        notify.enter_notify(token=token)
        return Response('호출에 성공했습니다!', status=status.HTTP_200_OK)


# 대기 등록 마감
class Breaktime(APIView):
    @swagger_auto_schema(tags=['Store'], manual_parameters=[header_authorization()])
    @transaction.atomic
    def patch(self, request):
        user = search_user(request)
        store_id = Store.objects.get(user_id=user.id).store_id
        try:
            object = Store.objects.get(store_id=store_id)
            object.is_waiting = not object.is_waiting
            result = object.is_waiting
            object.save()
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(data={"is_waiting": result}, status=status.HTTP_200_OK)


# 가게 상세 정보 수정
class Detail(APIView):
    @swagger_auto_schema(tags=['Store'], request_body=SwaggerStoreDetailSerializer, manual_parameters=[header_authorization()])
    @transaction.atomic
    def patch(self, request):
        user = search_user(request)
        store_id = Store.objects.get(user_id=user.id).store_id
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


# 대기 순서
def search_waiting_order(waiting_id, store_id):
    waiting_teams = Waiting.objects.filter(
        waiting_id__lt=waiting_id, store_id=store_id, status="WA")
    waiting_order = len(waiting_teams) + 1
    return waiting_order


# 대기자 입장, 대기자 조회
class Waitings(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(tags=['Store'], manual_parameters=[header_authorization()])
    @transaction.atomic
    def get(self, request):
        user = search_user(request)
        store_id = Store.objects.get(user_id=user.id).store_id
        data = search_waitings(store_id)
        return Response(data, status=status.HTTP_200_OK, content_type="text/json-comment-filtered")

    @swagger_auto_schema(tags=['Store'], request_body=SwaggerStoreWaitingsPatchSerializer,
                         manual_parameters=[header_authorization()])
    @transaction.atomic
    def patch(self, request):
        user = search_user(request)
        store_id = Store.objects.get(user_id=user.id).store_id
        waiting_id = request.data['waiting_id']
        waiting_order = search_waiting_order(waiting_id, store_id)
        try:
            waiting = Waiting.objects.get(waiting_id=waiting_id)
            waiting.status = 'EN'
            waiting.save()
            waitings = Waiting.objects.raw(
                """SELECT waiting_id, name, people, phone_num FROM Waiting WHERE store_id=%s AND status=%s LIMIT 1""" % (
                    store_id, "'WA'"))
            data = search_waitings(store_id)
            try:
                second_customer = Token.objects.get(
                    waiting_id=waitings[0]).token
                if waiting_order == 1:
                    notify.auto_notify(second_customer)
            except IndexError:
                pass
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(data, status=status.HTTP_200_OK)


# 웨이팅 강제 취소
class Cancellations(APIView):
    @swagger_auto_schema(tags=['Store'], request_body=SwaggerStoreWaitingsPatchSerializer,
                         manual_parameters=[header_authorization()])
    @transaction.atomic
    def patch(self, request):
        user = search_user(request)
        store_id = Store.objects.get(user_id=user.id).store_id
        waiting_id = request.data['waiting_id']
        waiting_order = search_waiting_order(waiting_id, store_id)
        cancel_token = Token.objects.get(waiting_id=waiting_id).token

        # status를 CN(CANCEL)로 바꿔주고 취소 알림 보내기
        Waiting.objects.filter(waiting_id=waiting_id,
                               store_id=store_id).update(status='CN')
        notify.cancel_notify(cancel_token)

        # 가게의 웨이팅 리스트, 상세 정보, 웨이팅 받는지 여부를 받아 온다.
        data = search_waitings(store_id)
        try:
            auto_token = Token.objects.get(
                waiting_id=data["data"][0]['waiting_id']).token

            # 취소한 웨이팅이 1순위였고 다음 웨이팅 팀이 존재할 경우 다음 팀에게 1순위 알림 보내기
            if waiting_order == 1:
                notify.auto_notify(auto_token)
        # 가게의 웨이팅이 없는 경우
        except IndexError:
            pass
        return Response(data, status=status.HTTP_200_OK, content_type="text/json-comment-filtered")


class Search(APIView):
    @swagger_auto_schema(tags=['Store'], request_body=SwaggerStoreSearchSerializer, manual_parameters=[header_authorization()])
    @transaction.atomic
    def post(self, request):
        user = search_user(request)
        latitude = float(request.data['latitude'])
        longitude = float(request.data['longitude'])
        query = """
                    SELECT store_id, ST_DistanceSphere(
                            ST_GeomFromText('POINT(' || a.longitude || ' ' || a.latitude || ')', 4326),
                            ST_GeomFromText('POINT(%s %s)', 4326)
                         ) as distance
                    FROM 
                        store as a
                    WHERE 
                        ST_DWithin(
                            ST_GeomFromText('POINT(' || a.longitude || ' ' || a.latitude || ')', 4326)::geography,
                            ST_GeomFromText('POINT(%s %s)', 4326)::geography,
                            3000
                            )
                    ORDER BY
                        distance"""
        with connection.cursor() as cursor:
            cursor.execute(
                query, [longitude, latitude, longitude, latitude]
            )
            result = cursor.fetchall()

        data = {"data": []}

        for i in result:
            store = Store.objects.get(store_id=i[0])
            temp = {
                "store_id": i[0],
                "store_name": store.store_name,
                "distance": i[1],
                "waiting": Waiting.objects.filter(store_id=store.store_id).count(),
                "is_waiting": store.is_waiting,
                "information": store.information,
                "latitude": store.latitude,
                "longitude": store.longitude
            }
            data["data"].append(temp)

        return Response(data, status=status.HTTP_200_OK)
