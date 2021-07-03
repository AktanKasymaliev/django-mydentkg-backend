from rest_framework import generics
from customUser.models import User
from rest_api.serializers.client_user_serializers import ClientUsersSerializer
from rest_api.send_mail import send_confirmation_email
from rest_framework import status, response

class ClientUsersView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = ClientUsersSerializer

class ClientUserRegisterView(generics.CreateAPIView):
    serializer_class = ClientUsersSerializer

    def post(self, request):
        serializer = ClientUsersSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            if user:
                send_confirmation_email(request, user)
                return response.Response(serializer.data, status=status.HTTP_201_CREATED)