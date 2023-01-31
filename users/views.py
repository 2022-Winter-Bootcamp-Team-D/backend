from django.contrib.auth import authenticate
from django.core.cache import cache
from django.db import transaction
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from swagger.serializer import SwaggerUserSignupSerializer, SwaggerUserSigninSerializer
from users.models import User
from users.serializer import SignupSerializer, SigninSerializer


class Signup(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(tags=['User'], request_body=SwaggerUserSignupSerializer)
    @transaction.atomic
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "register successs",
                    "access": access_token,
                },
                status=status.HTTP_201_CREATED,
            )
            cache.set(access_token, refresh_token, 60 * 60 * 3)
            return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Signin(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(tags=['User'], request_body=SwaggerUserSigninSerializer)
    @transaction.atomic
    def post(self, request):
        user = authenticate(
            email=request.data.get("email"), password=request.data.get("password")
        )
        if user is not None:
            user_data = User.objects.get(email=request.data.get("email"))
            serializer = SigninSerializer(user)
            role = user_data.role
            if role == 'auth':
                token = TokenObtainPairSerializer.get_token(user)
                refresh_token = str(token)
                access_token = str(token.access_token)
                res = Response(
                    {
                        "user": serializer.data,
                        "message": "login success",
                        "access": access_token,
                    },
                    status=status.HTTP_200_OK,
                )
                cache.set(access_token, refresh_token, 60*60*3)
                return res
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
