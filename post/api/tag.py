from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from post.api.utils import APIUtils
from post.serializers import TagSerializer


class TagAPI(APIView):
    def get(self, request: Request) -> Response:
        """
        Get the list of tags.
        """
        tags = APIUtils.get_list_of('Tag')
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)
