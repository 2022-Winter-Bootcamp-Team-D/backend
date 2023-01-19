from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        name = validated_data.get('name')
        phone_num = validated_data.get('phone_num')
        email = validated_data.get('email')
        password = validated_data.get('password')
        role = 'auth'
        user = User(
            name=name,
            phone_num=phone_num,
            email=email,
            role=role
        )
        user.set_password(password)
        user.save()
        return user


class StoreSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        name = validated_data.get('name')
        phone_num = validated_data.get('phone_num')
        email = validated_data.get('email')
        password = validated_data.get('password')
        role = 'store'
        user = User(
            name=name,
            phone_num=phone_num,
            email=email,
            role=role
        )
        user.set_password(password)
        user.save()
        return user
