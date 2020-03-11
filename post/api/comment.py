from typing import Any

from rest_framework import status  # type: ignore
from rest_framework.exceptions import NotFound, ParseError  # type: ignore
from rest_framework.response import Response  # type: ignore
from rest_framework.views import APIView  # type: ignore

from post.api.utils import APIUtils
from post.models import Comment
from post.serializers import CommentListSerializer, CommentSerializer


class CommentAPI(APIView):
    def get_object(self, comment_id: int) -> Comment:
        """
        Get a comment object.
        """
        try:
            return Comment.objects.get(pk=comment_id, is_active=True)
        except Exception:
            raise NotFound

    def comment_detail(self, comment_id: int) -> Response:
        """
        Get a comment.
        """
        comment = self.get_object(comment_id)
        serializer = CommentListSerializer(comment)

        return Response(serializer.data)

    def comment_list(self) -> Response:
        """
        Get a list of whole comments which are active
        """
        lists = Comment.objects.filter(is_active=True)
        serializer = CommentListSerializer(lists, many=True)

        return Response(serializer.data)

    def get(self, request: Any, **parameter: Any) -> Response:
        comment_id = parameter.get('comment_id')

        if comment_id:
            return self.comment_detail(comment_id)
        else:
            return self.comment_list()

    def post(self, request: Any) -> Response:
        """
        Create a comment.
        """
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        raise ParseError(detail=serializer.errors)

    def put(self, request: Any, comment_id: int) -> Response:
        """
        Update the comment's data.
        """
        APIUtils.validate(request.data)

        comment = self.get_object(comment_id)
        serializer = CommentSerializer(comment, request.data, partial=True)

        if serializer.is_valid():
            serializer.update(comment, request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return ParseError(detail=serializer.errors)

    def delete(self, request: Any, comment_id: int) -> Response:
        """
        Set a comment disabled
        """
        comment = self.get_object(comment_id)
        serializer = CommentSerializer(comment)
        serializer.update(comment, {'is_active': False})

        return Response(status=status.HTTP_204_NO_CONTENT)
