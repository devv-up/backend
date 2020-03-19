from typing import Optional

from rest_framework import status
from rest_framework.exceptions import ParseError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from post.api.utils import APIUtils
from post.serializers import TagSerializer


class TagAPI(APIView):
    def get(self, request: Request, **url_resources: Optional[int]) -> Response:
        """
        Gets a tag object or a list of tags.
        Basically, this function returns a response that include data of
        whole tags unless a specific tag id is given
        by uri resources.
        """
        tag_id = url_resources.get('tag_id')

        if tag_id:
            tag = APIUtils.get('Tag', id=tag_id)
            serializer = TagSerializer(tag)
            return Response(serializer.data)
        else:
            tags = APIUtils.get_list_of('Tag')
            serializer = TagSerializer(tags, many=True)
            return Response(serializer.data)

    def post(self, request: Request) -> Response:
        """
        Creates a tag.
        """
        serializer = TagSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        raise ParseError(detail=serializer.errors)

    def delete(self, request: Request, tag_id: int) -> Response:
        """
        Delete the tag.
        The specific tag ID must be required by uri resources.
        """
        tag = APIUtils.get('Tag', id=tag_id)
        tag.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
