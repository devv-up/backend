from typing import Optional

from rest_framework import status
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from post.models import Tag
from post.serializers import TagSerializer


class TagAPI(APIView):
    def get_object(self, tag_id: int) -> Tag:
        """
        Returns a tag object which is active.
        """
        try:
            return Tag.objects.get(pk=tag_id)
        except Exception:
            raise NotFound

    def tag_detail(self, tag_id: int) -> Response:
        """
        Gets a detailed tag.
        """
        tag = self.get_object(tag_id)
        serializer = TagSerializer(tag)

        return Response(serializer.data)

    def tag_list(self) -> Response:
        """
        Gets whole tags which are active.
        """
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)

        return Response(serializer.data)

    def get(self, request: Request, **url_resources: Optional[int]) -> Response:
        """
        Gets a tag object or a list of tags.
        Basically, this function returns a response that include data of
        whole tags unless a specific tag id is given
        by uri resources.
        """
        tag_id = url_resources.get('tag_id')

        if tag_id:
            return self.tag_detail(tag_id)
        else:
            return self.tag_list()

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
        tag = self.get_object(tag_id)
        tag.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
