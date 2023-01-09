from rest_framework import serializers
from waiting.models import Waiting


class WaitingSerializer(serializers.ModelSerializer):
    waiting_order = serializers.SerializerMethodField()

    def get_waiting_order(self, obj):
        return obj.waiting_order

    class Meta:
        model = Waiting
        fields = [
            'waiting_id',
            'waiting_order',
            'people',
            'create_at'
        ]

