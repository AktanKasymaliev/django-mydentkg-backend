from rest_api.permissions import IsOwnerOrReadOnly
from rest_framework import generics
from customUser.models import User
from rest_api.serializers.client_user_serializers import (ClientChangePasswordSerializer, ClientUsersSerializer,
                     ClientRegisterSerializer, ClientLoginSerializer)
from rest_api.send_mail import send_confirmation_email
from rest_framework import status, response
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.views import TokenObtainPairView

class ClientUsersView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = ClientUsersSerializer

    @swagger_auto_schema(operation_description='List client users', tags=['Client User'],
                         security=[])
    def get(self, request):
        return self.list(request)


class ClientUserRegisterView(generics.CreateAPIView):
    serializer_class = ClientRegisterSerializer

    @swagger_auto_schema(operation_description='Registration client user', tags=['Client User'],
                         security=[])
    def post(self, request):
        serializer = ClientRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            if user:
                send_confirmation_email(request, user)
                return response.Response(serializer.data, status=status.HTTP_201_CREATED)

class ClientLoginView(TokenObtainPairView):
    serializer_class = ClientLoginSerializer

    @swagger_auto_schema(operation_description='Login client users', tags=['Doctor User'],
                         security=[])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class ClientChangePasswordView(generics.UpdateAPIView):
    serializer_class = ClientChangePasswordSerializer
    model = User
    permission_classes = (IsOwnerOrReadOnly,)

    def update(self, request, *args, **kwargs):
        user = self.request.user
        serializer: ClientChangePasswordSerializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not user.check_password(serializer.data.get("old_password")):
                return response.Response({"old_password": "Wrong password"}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(serializer.data.get("new_password"))
            user.save()
            return response.Response({
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            })
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)