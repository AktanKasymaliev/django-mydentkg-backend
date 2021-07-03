from rest_framework import generics
from rest_api.serializers.doc_serializers import DoctorRegisterSerializer, DoctorUsersSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_api.send_mail import send_confirmation_email
from rest_framework import status
from doctorsUser.models import DoctorUser
from drf_yasg.utils import swagger_auto_schema

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
