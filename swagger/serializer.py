from rest_framework import serializers


class SwaggerWaitingListSerializer(serializers.Serializer):
    phone_num = serializers.CharField(help_text='phone_num')
    password = serializers.CharField(help_text='password')


class SwaggerWaitingsPatchSerializer(serializers.Serializer):
    waiting_id = serializers.IntegerField(help_text='waiting_id')
    store_id = serializers.IntegerField(help_text='store_id')


class SwaggerWaitingsPostSerializer(serializers.Serializer):
    store_id = serializers.IntegerField(help_text='store_id')
    phone_num = serializers.CharField(help_text='phone_num')
    password = serializers.CharField(help_text='password')
    name = serializers.CharField(help_text='name')
    people = serializers.IntegerField(help_text='people')
    token = serializers.CharField(help_text='token')


class SwaggerStoreSigninSerializer(serializers.Serializer):
    phone_num = serializers.CharField(help_text='phone_num')
    password = serializers.CharField(help_text='password')
    store_name = serializers.CharField(help_text='password')
    latitude = serializers.DecimalField(help_text='password', max_digits=10, decimal_places=6)
    longitude = serializers.DecimalField(help_text='password', max_digits=10, decimal_places=6)


class SwaggerStoreEnterNotifySerializer(serializers.Serializer):
    token = serializers.CharField(help_text='token')


class SwaggerStoreBreakTimeSerializer(serializers.Serializer):
    store_id = serializers.IntegerField(help_text='store_id')


class SwaggerStoreDetailSerializer(serializers.Serializer):
    store_id = serializers.IntegerField(help_text='store_id')
    information = serializers.CharField(help_text='information')


class SwaggerStoreWaitingsPostSerializer(serializers.Serializer):
    store_id = serializers.IntegerField(help_text='store_id')


class SwaggerStoreWaitingsPatchSerializer(serializers.Serializer):
    waiting_id = serializers.IntegerField(help_text='waiting_id')
    store_id = serializers.IntegerField(help_text='store_id')


class SwaggerStoreCancellationsSerializer(serializers.Serializer):
    waiting_id = serializers.IntegerField(help_text='waiting_id')
    store_id = serializers.IntegerField(help_text='store_id')
