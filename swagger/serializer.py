from drf_yasg import openapi
from rest_framework import serializers


# Waiting
class SwaggerWaitingsPostSerializer(serializers.Serializer):
    store_id = serializers.IntegerField(help_text='store_id')
    people = serializers.CharField(help_text='people')
    token = serializers.CharField(help_text='token')


# Store
class SwaggerStoreSignupSerializer(serializers.Serializer):
    phone_num = serializers.CharField(help_text='phone_num')
    password = serializers.CharField(help_text='password')
    name = serializers.CharField(help_text='name')
    email = serializers.EmailField(help_text='email', max_length=255)
    latitude = serializers.DecimalField(help_text='latitude', max_digits=10, decimal_places=6)
    longitude = serializers.DecimalField(help_text='longitude', max_digits=10, decimal_places=6)


class SwaggerStoreLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(help_text='email')
    password = serializers.CharField(help_text='password')


class SwaggerStoreEnterNotifySerializer(serializers.Serializer):
    token = serializers.CharField(help_text='token')


class SwaggerStoreDetailSerializer(serializers.Serializer):
    information = serializers.CharField(help_text='information')


class SwaggerStoreWaitingsPatchSerializer(serializers.Serializer):
    waiting_id = serializers.IntegerField(help_text='waiting_id')


class SwaggerStoreCancellationsSerializer(serializers.Serializer):
    waiting_id = serializers.IntegerField(help_text='waiting_id')


# User
class SwaggerUserSignupSerializer(serializers.Serializer):
    name = serializers.CharField(help_text='store_name')
    password = serializers.CharField(help_text='password')
    email = serializers.EmailField(help_text='email')
    phone_num = serializers.CharField(help_text='phone_num')


class SwaggerUserSigninSerializer(serializers.Serializer):
    email = serializers.EmailField(help_text='email')
    password = serializers.CharField(help_text='password')


# Header
def get_token():
    parameter_token = openapi.Parameter(
        "Authorization",
        openapi.IN_HEADER,
        description="access_token",
        type=openapi.TYPE_STRING
    )
    return parameter_token
