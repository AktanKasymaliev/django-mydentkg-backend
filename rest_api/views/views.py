from rest_framework import response, status
from rest_framework.views import APIView
from doctorsUser.models import DoctorUser, Reception, Reserve
from comments.models import Comments
from rest_api.serializers.serializers import CommentSerializer, CommentsAddSerializers, MakeReserverSerializer, ReceptionAddSerializer, ReceptionSerializer, ReservedSerializers
from rest_framework import generics, permissions
from drf_yasg.utils import swagger_auto_schema

class CommentsView(generics.ListAPIView):
    serializer_class = CommentSerializer
    queryset = Comments.objects.all()

    @swagger_auto_schema(operation_description='List comments', tags=['Comments'],
                         security=[])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class CommentAddView(generics.CreateAPIView):
    serializer_class = CommentsAddSerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Comments.objects.all()

    def get_serializer_context(self):
        return {'request': self.request}
    
    @swagger_auto_schema(operation_description='Add comments', tags=['Comments'],
                         security=[])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class ReceptionView(generics.ListAPIView):
    queryset = Reception.objects.select_related('doctor')
    serializer_class = ReceptionSerializer

    @swagger_auto_schema(operation_description='List free times', tags=['Reception'],
                         security=[])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
class ReceptionAddView(generics.CreateAPIView):
    serializer_class = ReceptionAddSerializer
    queryset = Reception.objects.select_related('doctor')

    def get_serializer_context(self):
        return {'request': self.request}

    @swagger_auto_schema(operation_description='Add free times', tags=['Reception'],
                         security=[])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class ReservedView(generics.ListAPIView):
    serializer_class = ReservedSerializers
    queryset = Reserve.objects.select_related('doctor')

    @swagger_auto_schema(operation_description='Reserved free times', tags=['Reception'],
                         security=[])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class MakeReserveView(generics.CreateAPIView):
    serializer_class = MakeReserverSerializer
    queryset = Reserve.objects.select_related('doctor')

    def get_serializer_context(self):
        return {'request': self.request}

    @swagger_auto_schema(operation_description='Reserve free times', tags=['Reception'],
                         security=[])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class CategoryListView(APIView):

    def get(self, request, category):
        try:
            doctors = DoctorUser.objects.filter(profession=category)
            if doctors.count() == 0:
                return response.Response({category: "В данной специализации отстутсвуют специалисты"}, status=status.HTTP_404_NOT_FOUND)
            return response.Response({category: doctors}, status=status.HTTP_200_OK)
        except DoctorUser.DoesNotExist:
            return response.Response({category: "В данной специализации отстутсвуют специалисты"}, status=status.HTTP_404_NOT_FOUND)
        