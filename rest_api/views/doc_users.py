from rest_framework import generics
from rest_framework import response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_api.serializers.doc_serializers import (DoctorRegisterSerializer,
                DoctorUsersSerializer, DoctorLoginSerializer, DoctorChangePasswordSerializer)
from rest_framework.response import Response
from rest_api.send_mail import password_reset_token_created, send_confirmation_email
from rest_framework import status
from doctorsUser.models import DoctorUser
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.backends import TokenBackend
from rest_api.permissions import IsOwnerOrReadOnly
import jwt
from config.settings import SECRET_KEY

class DoctorUsersView(generics.ListAPIView):
    queryset = DoctorUser.objects.all()
    serializer_class = DoctorUsersSerializer

    @swagger_auto_schema(operation_description='List doctor users (can add params(?search) for search)', tags=['Doctor User'],
                         security=[])
    def get(self, request):
        return self.list(request)
    
    def get_queryset(self):
        search = self.request.query_params.get("search")
        query = super().get_queryset()
        if search:
            query = query.filter(fullname__icontains=search)
            return query
        else:
            return query

class Doctor(generics.RetrieveAPIView):
    serializer_class = DoctorUsersSerializer
    queryset = DoctorUser.objects.all()

class DoctorUserRegisterView(generics.CreateAPIView):
    serializer_class = DoctorRegisterSerializer

    @swagger_auto_schema(operation_description='Registration doctor users', tags=['Doctor User'],
                         security=[])
    def post(self, request):
        serializer = DoctorRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            if user:
                send_confirmation_email(request, user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

class DoctorLoginView(TokenObtainPairView):
    serializer_class = DoctorLoginSerializer
    permission_classes = [AllowAny,]
    
    @swagger_auto_schema(operation_description='Login doctor users', tags=['Doctor User'],
                         security=[])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class DoctorChangePasswordView(generics.UpdateAPIView):
    serializer_class = DoctorChangePasswordSerializer
    model = DoctorUser
    permission_classes = (IsOwnerOrReadOnly,)

    def update(self, request, *args, **kwargs):
        user = self.request.user
        serializer: DoctorChangePasswordSerializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not user.check_password(serializer.data.get("old_password")):
                return Response({"old_password": "Wrong password"}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(serializer.data.get("new_password"))
            user.save()
            return Response({
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DoctorForgotPasswordView(APIView):
    permission_classes = [IsOwnerOrReadOnly, ]

    @swagger_auto_schema(operation_description='Reset password doctor users', tags=['Doctor User'],
                         security=[])
    def get(self, request, *args, **kwargs):
        password_reset_token_created(request)
        return response.Response("Email was sended", status=status.HTTP_200_OK)
    
class DoctorInfo(generics.ListAPIView):
    serializer_class = DoctorUsersSerializer
    model = DoctorUser
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
        user_id = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])["user_id"]
        request.user = DoctorUser.objects.get(pk=user_id)
        try:
            data = {
                "id": str(request.user.id),
                "fullname": str(request.user.fullname),
                "username": str(request.user.username),
                "email": str(request.user.email),
                "phone_number": str(request.user.phone_number),
                "license_image": str(request.user.license_image),
                "avatar": str(request.user.avatar),
                "profession": str(request.user.profession),
                "experience": str(request.user.experience),
                "price": str(request.user.price),
                "company": str(request.user.company),
                "address": str(request.user.address),
                "is_active": str(request.user.is_active),
            }
            return response.Response(data, status=200)
        except Exception:
            return response.Response("Login does not succeded", status=401)