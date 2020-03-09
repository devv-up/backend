from typing import Any

from rest_framework import status  # type: ignore
from rest_framework.exceptions import NotFound, ParseError  # type: ignore
from rest_framework.response import Response  # type: ignore
from rest_framework.views import APIView  # type: ignore

from post.models import Tag
from post.serializers import TagSerializer


class TagAPI(APIView):
    def get_object(self, tag_id: int) -> Tag:
        """
        Get a tag object.
        """
        try:
            return Tag.objects.get(pk=tag_id)
        except Exception:
            raise NotFound

    def tag_detail(self, tag_id: int) -> Response:
        """
        Get a tag.
        """
        tag = self.get_object(tag_id)
        serializer = TagSerializer(tag)

        return Response(serializer.data)

    def tag_list(self) -> Response:
        """
        Get a list of whole tags which are active.
        """
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)

        return Response(serializer.data)

    def get(self, request: Any, **parameter: Any) -> Response:
        tag_id = parameter.get('tag_id')

        if tag_id:
            return self.tag_detail(tag_id)
        else:
            return self.tag_list()

    def post(self, request: Any) -> Response:
        """
        Create a tag.
        """
        serializer = TagSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        raise ParseError(detail=serializer.errors)

    def put(self, request: Any, tag_id: int) -> Response:
        """
        Update the tag title.
        """
        tag = self.get_object(tag_id)
        serializer = TagSerializer(tag, request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        raise ParseError(detail=serializer.errors)

    def delete(self, request: Any, tag_id: int) -> Response:
        """
        Delete a tag.
        """
        tag = self.get_object(tag_id)
        tag.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
