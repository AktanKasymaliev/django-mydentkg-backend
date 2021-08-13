from django.db import models
from rest_framework import serializers
from doctorsUser.models import DoctorUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .serializers import ReceptionSerializer, ReservedSerializers

class DoctorUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorUser
        fields = ('id', "fullname", "username",
        "email", "phone_number", 'avatar',
        "profession", "experience", "price",
        "company", "address", "is_active")

    def to_representation(self, instance):
        representation = super(DoctorUsersSerializer, self).to_representation(instance)
        representation['free_times'] = ReceptionSerializer(instance.time.all(), many=True).data
        representation['reserved_time'] = ReservedSerializers(instance.reserve.all(), many=True).data
        return representation


class DoctorRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, required=True, write_only=True)

    class Meta:
        model = DoctorUser
        fields = ('username', "email",
        "phone_number", "license_image",
        "password", "fullname", "avatar",
         "profession", "experience", "price",
         "company", "address")

    def create(self, validated_data):
        user = DoctorUser.objects.create_user(**validated_data)
        return user

class DoctorLoginSerializer(TokenObtainPairSerializer):
    password = serializers.CharField(min_length=6, write_only=True)

    def validate(self, validated_data):
        email = validated_data.get('email')

        password = validated_data.pop('password', None)
        if not DoctorUser.objects.filter(email=email).exists():
            raise serializers.ValidationError(_('User not found'))
        user = authenticate(username=email, password=password)
        if user and user.is_active:
            refresh = self.get_token(user)
            validated_data['refresh'] = str(refresh)
            validated_data['access'] = str(refresh.access_token)
            validated_data['user'] = DoctorUsersSerializer(instance=user).data
        return validated_data


class DoctorChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password_confirm = serializers.CharField(required=True)

    def validate(self, validated_data):
        new_password = validated_data.get('new_password')
        new_password_confirm = validated_data.get('new_password_confirm')
        if new_password != new_password_confirm:
            raise serializers.ValidationError(_('Passwords don\'t match'))
        return validated_data

    