from typing import Optional

from rest_framework import status
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from post.api.utils import APIUtils
from post.models import Comment
from post.serializers import CommentListSerializer, CommentSerializer


class CommentAPI(APIView):
    def get_object(self, comment_id: int) -> Comment:
        """
        Returns a comment object which is active.
        """
        try:
            return Comment.objects.get(pk=comment_id, is_active=True)
        except Exception:
            raise NotFound

    def comment_detail(self, comment_id: int) -> Response:
        """
        Gets a detailed comment.
        """
        comment = self.get_object(comment_id)
        serializer = CommentListSerializer(comment)

        return Response(serializer.data)

    def comment_list(self) -> Response:
        """
        Gets whole comments which are active
        """
        lists = Comment.objects.filter(is_active=True)
        serializer = CommentListSerializer(lists, many=True)

        return Response(serializer.data)

    def get(self, request: Request, **url_resources: Optional[int]) -> Response:
        """
        Gets a comment object or a list of categories.
        Basically, this function returns a response that include data of
        whole comments unless a specific comment id is given
        by uri resources.
        """
        comment_id = url_resources.get('comment_id')

        if comment_id:
            return self.comment_detail(comment_id)
        else:
            return self.comment_list()

    def post(self, request: Request) -> Response:
        """
        Creates a comment.
        """
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        raise ParseError(detail=serializer.errors)

    def put(self, request: Request, comment_id: int) -> Response:
        """
        Update the comment's data.
        The specific comment ID must be required by uri resources.
        """
        APIUtils.validate(request.data)

        comment = self.get_object(comment_id)
        serializer = CommentSerializer(comment, request.data, partial=True)

        if serializer.is_valid():
            serializer.update(comment, request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        raise ParseError(detail=serializer.errors)

    def delete(self, request: Request, comment_id: int) -> Response:
        """
        Makes the comment disabled.
        The specific comment ID must be required by uri resources.
        """
        comment = self.get_object(comment_id)
        serializer = CommentSerializer(comment)
        serializer.update(comment, {'is_active': False})

        return Response(status=status.HTTP_204_NO_CONTENT)
