from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from post.models import Tag
from post.serializers import TagSerializer


class TagAPI(viewsets.ViewSet):
    def list(self, request: Request) -> Response:
        """
        Get the list of tags.
        """
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)
