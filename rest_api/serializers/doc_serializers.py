from django.db import models
from rest_framework import serializers
from doctorsUser.models import DoctorUser

class DoctorUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorUser
        fields = ('id', "fullname", "username",
        "email", "phone_number", 'avatar',
        "profession", "experience", "price",
        "company", "address", "is_active")

    def to_representation(self, instance):
        representation = super(DoctorUsersSerializer, self).to_representation(instance)
        return representation

class DoctorRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, required=True, write_only=True)

    class Meta:
        model = DoctorUser
        fields = ('username', "email")

    def create(self, validated_data):
        user = DoctorUser.objects.create_user(**validated_data)
        return user