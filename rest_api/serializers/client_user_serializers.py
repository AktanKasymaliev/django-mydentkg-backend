from rest_framework import serializers
from customUser.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

class ClientUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', "username",
        "email", "phone_number", "is_active")

class ClientRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, required=True, write_only=True)

    class Meta:
        model = User
        fields = ('username', "email",
        "phone_number",
        "password")

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class ClientLoginSerializer(TokenObtainPairSerializer):
    password = serializers.CharField(min_length=6, write_only=True)

    def validate(self, validated_data):
        email = validated_data.get('email')

        password = validated_data.pop('password', None)
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError(_('User not found'))
        user = authenticate(username=email, password=password)
        if user and user.is_active:
            refresh = self.get_token(user)
            validated_data['refresh'] = str(refresh)
            validated_data['access'] = str(refresh.access_token)
            validated_data['user'] = ClientUsersSerializer(instance=user).data
        return validated_data