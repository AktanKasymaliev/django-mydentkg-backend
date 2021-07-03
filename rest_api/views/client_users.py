from rest_framework import generics
from customUser.models import User
from rest_api.serializers.client_user_serializers import ClientUsersSerializer

class ClientUsersView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = ClientUsersSerializer