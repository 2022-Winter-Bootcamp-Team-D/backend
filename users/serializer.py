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
        user = User(
            name=name,
            phone_num=phone_num,
            email=email
        )
        user.set_password(password)
        user.save()
        return user


class SigninSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

