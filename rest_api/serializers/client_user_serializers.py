from rest_framework import serializers
from customUser.models import User

class ClientUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', "username",
        "email", "phone_number", "is_active")