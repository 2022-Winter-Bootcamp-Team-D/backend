from rest_framework import serializers
from store.models import Store


class StoreJoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ('store_id',)
