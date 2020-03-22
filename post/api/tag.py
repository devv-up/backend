from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from post.api.utils import APIUtils
from post.serializers import TagSerializer


class TagAPI(APIView):
    def get(self, request: Request, tag_id: int = None) -> Response:
        """
        Get a tag object or the list of tags.
        Basically, this function returns a response that includes data of
        whole tags unless a specific tag ID is given
        by uri resources.
        """
        if tag_id:
            tag = APIUtils.get('Tag', id=tag_id)
            serializer = TagSerializer(tag)
            return Response(serializer.data)
        else:
            tags = APIUtils.get_list_of('Tag')
            serializer = TagSerializer(tags, many=True)
            return Response(serializer.data)
