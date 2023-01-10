from rest_framework import serializers
from store.models import Store
from waiting.models import Waiting


class StoreJoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ('store_id',)


class StoreBreaktimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ('is_waiting',)


class StoreDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ('information',)


class StoreWaitingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Waiting
        fields = [
            'name',
            'phone_num',
            'people'
        ]
