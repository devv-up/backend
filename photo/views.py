from rest_framework import viewsets

from photo.models import photo
from photo.serializers import ImageSerializer

# Create your views here.


class PhotoViewSet(viewsets.ModelViewSet):

    queryset = photo.objects.all()
    serializer_class = ImageSerializer
