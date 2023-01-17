from rest_framework import serializers
from store.models import Store
from waiting.models import Waiting
from users.models import User


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
        fields = ('information', )


class StoreWaitingsSerializer(serializers.ModelSerializer):
    information = serializers.SerializerMethodField()
    is_waiting = serializers.SerializerMethodField()

    def get_information(self, obj):
        return obj.information

    def get_is_waiting(self, obj):
        return obj.is_waiting

    class Meta:
        model = Waiting
        fields = [
            'information',
            'is_waiting',
            'waiting_id',
            'name',
            'people',
            'phone_num'
        ]
