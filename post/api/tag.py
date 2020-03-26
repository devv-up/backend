from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from post.models import Tag
from post.serializers import TagSerializer


class TagAPI(APIView):
    def get(self, request: Request) -> Response:
        """
        Get the list of tags.
        """
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)
