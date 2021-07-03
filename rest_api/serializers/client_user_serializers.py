from rest_framework import serializers
from customUser.models import User

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