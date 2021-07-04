from rest_framework import generics, permissions

from rest_api.permissions import IsOwner
from ratings.models import Rating
from ratings.serializers import RatingAddSerializer

class RatingAddView(generics.ListCreateAPIView):
    queryset = Rating.objects.select_related("author")
    serializer_class = RatingAddSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_serializer_context(self):
        return {'request': self.request}

class RatingRemove(generics.DestroyAPIView):
    permission_classes = [IsOwner]
    queryset = Rating.objects.select_related("author")

    def delete(self, request, pk):
        return super().delete(request, pk)