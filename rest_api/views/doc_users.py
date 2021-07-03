from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_api.serializers.doc_serializers import (DoctorRegisterSerializer,
                DoctorUsersSerializer, DoctorLoginSerializer, DoctorChangePasswordSerializer)
from rest_framework.response import Response
from rest_api.send_mail import send_confirmation_email
from rest_framework import status
from doctorsUser.models import DoctorUser
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_api.permissions import IsOwnerOrReadOnly

class DoctorUsersView(generics.ListAPIView):
    queryset = DoctorUser.objects.all()
    serializer_class = DoctorUsersSerializer

    @swagger_auto_schema(operation_description='List doctor users', tags=['Doctor User'],
                         security=[])
    def get(self, request):
        return self.list(request)

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
        print(user)
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