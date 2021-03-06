from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_api.permissions import IsOwnerOrReadOnly
from rest_framework import generics
from customUser.models import User
from rest_api.serializers.client_user_serializers import (ClientChangePasswordSerializer, 
                     ClientUsersSerializer,
                     ClientRegisterSerializer, ClientLoginSerializer)
from rest_api.send_mail import send_confirmation_email, password_reset_token_created
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

    @swagger_auto_schema(operation_description='Login client users', tags=['Client User'],
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


class ClientForgotPasswordView(APIView):
    permission_classes = [IsOwnerOrReadOnly, ]

    @swagger_auto_schema(operation_description='Reset password client users', tags=['Client User'],
                         security=[])
    def get(self, request, *args, **kwargs):
        password_reset_token_created(request)
        return response.Response("Email was sended", status=status.HTTP_200_OK)

class ClientInfo(generics.ListAPIView):
    model = User
    serializer_class = ClientUsersSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            data = {
                "id": request.user.id,
                "username": request.user.username,
                "email": request.user.email,
                "phone_number": request.user.phone_number,
                "is_active": request.user.is_active,
            }
            return response.Response(data, status=200)
        except:
            return response.Response("Login does not succeded", status=401)