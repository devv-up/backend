from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from post.models import Tag
from post.serializers import TagSerializer


class TagAPI(viewsets.ViewSet):
    list_response = openapi.Response('**Success**', TagSerializer(many=True))

    @swagger_auto_schema(responses={200: list_response})
    def list(self, request: Request) -> Response:
        """
        Get the list of tags.
        """
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)
