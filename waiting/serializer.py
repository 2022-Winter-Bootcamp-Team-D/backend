from rest_framework import serializers
from waiting.models import Waiting


class WaitingSerializer(serializers.ModelSerializer):
    waiting_order = serializers.SerializerMethodField()
    store_name = serializers.SerializerMethodField()

    def get_waiting_order(self, obj):
        return obj.waiting_order

    def get_store_name(self, obj):
        return obj.store_name

    class Meta:
        model = Waiting
        fields = [
            'waiting_id',
            'store_name',
            'waiting_order',
            'people',
            'create_at'
        ]
